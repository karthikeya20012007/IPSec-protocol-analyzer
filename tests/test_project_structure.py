import os
import pytest

def test_required_scripts_exist_and_executable():
    """Verify that the required testbed scripts exist and are executable."""
    scripts = [
        "scripts/setup_testbed.sh",
        "scripts/cleanup_testbed.sh",
        "scripts/verify_testbed.sh",
        "scripts/setup_dev.sh",
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Required script {script} is missing."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_required_configs_exist():
    """Verify that the required strongSwan configurations exist."""
    configs = [
        "conf/gateway-a/swanctl.conf",
        "conf/gateway-b/swanctl.conf",
    ]
    for conf in configs:
        assert os.path.isfile(conf), f"Required configuration {conf} is missing."

def test_readme_exists():
    """Verify that documentation exists."""
    assert os.path.isfile("README.md"), "README.md is missing."
    assert os.path.isfile("docs/setup.md"), "docs/setup.md is missing."
