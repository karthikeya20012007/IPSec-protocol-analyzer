# IPSec Protocol Analyzer

## Overview
An AI-driven IPsec protocol analysis platform for testbed control, packet capture, protocol feature extraction, and ML-based encrypted traffic classification.

## Project Structure
- `scripts/`: Shell scripts for setting up, verifying, and cleaning up the IPsec testbed.
- `conf/`: Configuration files (e.g., `swanctl.conf`) for the IPsec endpoints.
- `tests/`: Automated test suite (`pytest`).
- `docs/`: Project documentation.
- `dataset/`: Directory for storing captured PCAPs and extracted features (ignored in git).

## Environment Setup
See [Development Guide](docs/development.md) for details on setting up the local Python virtual environment and dependencies.

## IPsec Testbed
The project uses Linux network namespaces to simulate a complete IPsec topology on a single host. 
See [Testbed Documentation](docs/testbed.md) for network topology details and configuration instructions.

## Testing
We use `pytest` for all automated tests.
To run safe tests (non-privileged):
```bash
pytest -m "not requires_root"
```

To run integration tests (requires root and strongSwan):
```bash
sudo pytest -m requires_root
```

## CI/CD
GitHub Actions is configured to automatically run the safe test suite on pushes and pull requests.
Integration tests that require root privileges and specific kernel modules are separated and must be verified locally or on specialized runners.
