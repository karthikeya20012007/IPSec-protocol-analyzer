#!/bin/bash
set -euo pipefail

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (or with sudo)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "[*] Cleaning up any existing testbed..."
"${SCRIPT_DIR}/cleanup_testbed.sh" || true

echo "[*] Creating network namespaces..."
ip netns add client
ip netns add gateway-a
ip netns add gateway-b
ip netns add server

echo "[*] Creating veth pairs..."
ip link add veth_c_a type veth peer name veth_a_c
ip link add veth_a_b type veth peer name veth_b_a
ip link add veth_b_s type veth peer name veth_s_b

echo "[*] Assigning interfaces to namespaces..."
ip link set veth_c_a netns client
ip link set veth_a_c netns gateway-a

ip link set veth_a_b netns gateway-a
ip link set veth_b_a netns gateway-b

ip link set veth_b_s netns gateway-b
ip link set veth_s_b netns server

echo "[*] Configuring IP addresses and bringing up interfaces..."
# Client
ip netns exec client ip addr add 10.0.1.2/24 dev veth_c_a
ip netns exec client ip link set veth_c_a up
ip netns exec client ip link set lo up
ip netns exec client ip route add default via 10.0.1.1

# Gateway A
ip netns exec gateway-a ip addr add 10.0.1.1/24 dev veth_a_c
ip netns exec gateway-a ip link set veth_a_c up
ip netns exec gateway-a ip addr add 192.168.1.1/24 dev veth_a_b
ip netns exec gateway-a ip link set veth_a_b up
ip netns exec gateway-a ip link set lo up
ip netns exec gateway-a sysctl -w net.ipv4.ip_forward=1

# Gateway B
ip netns exec gateway-b ip addr add 192.168.1.2/24 dev veth_b_a
ip netns exec gateway-b ip link set veth_b_a up
ip netns exec gateway-b ip addr add 10.0.2.1/24 dev veth_b_s
ip netns exec gateway-b ip link set veth_b_s up
ip netns exec gateway-b ip link set lo up
ip netns exec gateway-b sysctl -w net.ipv4.ip_forward=1

# Server
ip netns exec server ip addr add 10.0.2.2/24 dev veth_s_b
ip netns exec server ip link set veth_s_b up
ip netns exec server ip link set lo up
ip netns exec server ip route add default via 10.0.2.1

echo "[*] Routing configured."

echo "[*] Preparing strongSwan configuration in namespaces..."
# Safely bind-mount /etc/swanctl and override strongswan.conf for each namespace
for GW in gateway-a gateway-b; do
    mkdir -p "/etc/netns/${GW}/swanctl"
    if [ -d /etc/swanctl ]; then
        cp -a /etc/swanctl/* "/etc/netns/${GW}/swanctl/" 2>/dev/null || true
    fi
    cp "${PROJECT_DIR}/conf/${GW}/swanctl.conf" "/etc/netns/${GW}/swanctl/swanctl.conf"
    
    # Create custom strongswan.conf to isolate VICI sockets
    cat <<EOF > "/etc/netns/${GW}/strongswan.conf"
charon {
    load_modular = yes
    plugins {
        include strongswan.d/charon/*.conf
        vici {
            socket = unix:///var/run/charon-${GW}.vici
        }
    }
}
include strongswan.d/*.conf
swanctl {
    socket = unix:///var/run/charon-${GW}.vici
}
EOF
done

echo "[*] Starting strongSwan in namespaces..."
# charon-systemd is the standard daemon in modern Ubuntu when strongswan-starter isn't used
CHARON_BIN="/usr/sbin/charon-systemd"
if [ ! -x "$CHARON_BIN" ]; then
    echo "ERROR: $CHARON_BIN not found or not executable."
    exit 1
fi
echo "[*] Using daemon: $CHARON_BIN"

# Run charon-systemd in the background. It doesn't fork by default.
ip netns exec gateway-a "$CHARON_BIN" > /var/log/charon-gateway-a.log 2>&1 &
echo $! > /var/run/charon-gateway-a.pid

ip netns exec gateway-b "$CHARON_BIN" > /var/log/charon-gateway-b.log 2>&1 &
echo $! > /var/run/charon-gateway-b.pid

echo "[*] Waiting for charon to be ready..."
for i in {1..10}; do
    if ip netns exec gateway-a swanctl --stats >/dev/null 2>&1 && \
       ip netns exec gateway-b swanctl --stats >/dev/null 2>&1; then
        echo "[*] Charon daemons are ready."
        break
    fi
    if [ "$i" -eq 10 ]; then
        echo "ERROR: Charon daemons did not become ready."
        cat /var/log/charon-gateway-a.log || true
        exit 1
    fi
    sleep 1
done

echo "[*] Loading swanctl configurations..."
ip netns exec gateway-a swanctl --load-all
ip netns exec gateway-b swanctl --load-all

echo "[*] Initiating IPsec connection..."
ip netns exec gateway-a swanctl --initiate --child net-net

echo "[*] Waiting for tunnel to establish..."
sleep 2

echo "[*] Testbed setup complete."
