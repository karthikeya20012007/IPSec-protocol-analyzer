# Development Guide

## Local Environment Setup

1. **Virtual Environment:**
   Create a local Python virtual environment to isolate project dependencies.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Dependencies:**
   Install the development dependencies.
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **System Dependencies:**
   For Phase 1 (Local Testbed), you must install the following system packages manually (e.g., on Ubuntu):
   ```bash
   sudo apt-get update
   sudo apt-get install strongswan strongswan-swanctl charon-systemd tshark
   ```

## Testing

Run tests using pytest:
```bash
pytest
```

Integration tests requiring root privileges will be skipped automatically if run as a normal user. To run them, ensure your environment is set up and execute tests with `sudo` (adjusting the PATH so root can find pytest).
