#!/bin/bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (or with sudo)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PCAP_DIR="${PROJECT_DIR}/dataset/ipsec/raw"
mkdir -p "$PCAP_DIR"
PCAP_FILE="${PCAP_DIR}/test.pcap"

echo "=== IKE and CHILD SA Status ==="
ip netns exec gateway-a swanctl --list-sas

echo "=== XFRM Policies ==="
ip netns exec gateway-a ip xfrm policy

echo "=== XFRM State ==="
ip netns exec gateway-a ip xfrm state

echo "=== Starting Traffic Capture ==="
# Capture on the external interface between gateway A and B
ip netns exec gateway-a tcpdump -ni veth_a_b 'esp or udp port 500 or udp port 4500' -c 10 -w "$PCAP_FILE" >/dev/null 2>&1 &
TCPDUMP_PID=$!
sleep 1

echo "=== Generating Traffic (Client to Server) ==="
# We check if ping succeeds
if ip netns exec client ping -c 5 10.0.2.2; then
    echo "[+] Client-to-Server Ping: SUCCESS"
else
    echo "[-] Client-to-Server Ping: FAILED"
    exit 1
fi

echo "=== Waiting for Capture ==="
wait $TCPDUMP_PID || true

echo "=== Analyzing Capture ==="
ESP_PKTS=$(tshark -r "$PCAP_FILE" -Y "esp" 2>/dev/null | wc -l || true)
IKE_PKTS=$(tshark -r "$PCAP_FILE" -Y "isakmp" 2>/dev/null | wc -l || true)
UDP_ENCAP_PKTS=$(tshark -r "$PCAP_FILE" -Y "udp.port==4500" 2>/dev/null | wc -l || true)

echo "IKE Packets: $IKE_PKTS"
echo "ESP Packets: $ESP_PKTS"
echo "NAT-T ESP Packets: $UDP_ENCAP_PKTS"

if [ "$ESP_PKTS" -gt 0 ] || [ "$UDP_ENCAP_PKTS" -gt 0 ]; then
    echo "[+] SUCCESS: Encrypted ESP/NAT-T traffic observed."
else
    echo "[-] FAILURE: No ESP or NAT-T traffic detected in the capture."
    exit 1
fi

echo "=== Phase 1 Verification Script Complete ==="
