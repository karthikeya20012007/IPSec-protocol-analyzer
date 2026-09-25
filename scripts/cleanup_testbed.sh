#!/bin/bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (or with sudo)"
  exit 1
fi

echo "[*] Killing charon instances..."
for GW in gateway-a gateway-b; do
    if [ -f "/var/run/charon-${GW}.pid" ]; then
        kill "$(cat "/var/run/charon-${GW}.pid")" 2>/dev/null || true
        rm -f "/var/run/charon-${GW}.pid"
    fi
done
# Also catch-all just in case
pkill -f "charon-systemd" || true

echo "[*] Deleting network namespaces (this will also delete the associated veth interfaces)..."
ip netns del client 2>/dev/null || true
ip netns del gateway-a 2>/dev/null || true
ip netns del gateway-b 2>/dev/null || true
ip netns del server 2>/dev/null || true

echo "[*] Cleaning up configuration and runtime files..."
rm -rf /etc/netns/gateway-a 2>/dev/null || true
rm -rf /etc/netns/gateway-b 2>/dev/null || true
rm -f /var/run/charon-gateway-a.vici 2>/dev/null || true
rm -f /var/run/charon-gateway-b.vici 2>/dev/null || true
rm -f /var/log/charon-gateway-a.log 2>/dev/null || true
rm -f /var/log/charon-gateway-b.log 2>/dev/null || true

echo "[*] Cleanup complete."
