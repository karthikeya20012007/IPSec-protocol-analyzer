#!/bin/bash
set -euo pipefail

# Safe, idempotent developer environment setup.
#
# This script:
#   1. Checks Python version
#   2. Creates .venv if missing
#   3. Installs requirements-dev.txt
#   4. Runs a basic pytest check
#   5. Reports missing system packages
#
# This script does NOT:
#   - Create or read SSH keys
#   - Modify GitHub settings or store credentials
#   - Install system packages (reports what is missing)
#   - Modify /etc/wsl.conf or Windows networking
#   - Commit or push to Git

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== IPSec Protocol Analyzer — Developer Setup ==="
echo ""

# --- 1. Check Python version ---
echo "[1/5] Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.12+."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "  Found: $PYTHON_VERSION"

# --- 2. Create venv if missing ---
echo "[2/5] Virtual environment..."
VENV_DIR="${PROJECT_DIR}/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "  .venv already exists."
else
    echo "  Creating .venv..."
    python3 -m venv "$VENV_DIR"
    echo "  Created."
fi

# --- 3. Install dependencies ---
echo "[3/5] Installing development dependencies..."
"${VENV_DIR}/bin/python" -m pip install --upgrade pip --quiet
"${VENV_DIR}/bin/pip" install -r "${PROJECT_DIR}/requirements-dev.txt" --quiet
echo "  Done."

# --- 4. Verify pytest ---
echo "[4/5] Verifying pytest..."
PYTEST_VERSION=$("${VENV_DIR}/bin/python" -m pytest --version 2>&1 | head -1)
echo "  $PYTEST_VERSION"

echo "  Running quick test collection..."
"${VENV_DIR}/bin/python" -m pytest "${PROJECT_DIR}" --collect-only --quiet 2>&1 | tail -3
echo ""

# --- 5. Check system packages ---
echo "[5/5] Checking system packages..."
MISSING=()
REQUIRED_CMDS=(
    "swanctl:strongswan-swanctl"
    "charon-systemd:charon-systemd"
    "tshark:tshark"
    "ip:iproute2"
    "tcpdump:tcpdump"
    "hping3:hping3"
    "iperf3:iperf3"
)

for entry in "${REQUIRED_CMDS[@]}"; do
    CMD="${entry%%:*}"
    PKG="${entry##*:}"
    if command -v "$CMD" &>/dev/null || [ -x "/usr/sbin/$CMD" ]; then
        echo "  ✓ $CMD"
    else
        echo "  ✗ $CMD  (install: sudo apt-get install $PKG)"
        MISSING+=("$PKG")
    fi
done

echo ""

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Missing system packages detected. Install them with:"
    echo ""
    echo "  sudo apt-get update"
    echo "  sudo apt-get install -y ${MISSING[*]}"
    echo ""
    echo "This script does not install system packages automatically."
else
    echo "All system packages are installed."
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Activate the virtual environment with:"
echo "  source .venv/bin/activate"
echo ""
echo "See docs/setup.md for the full setup guide."
