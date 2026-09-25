import subprocess
import pytest
import os

@pytest.mark.integration
@pytest.mark.requires_root
@pytest.mark.requires_ipsec
def test_ipsec_testbed():
    """
    Integration test to verify that the IPsec testbed can be brought up,
    traffic is encrypted (ESP), and then cleanly torn down.
    This test requires root privileges and strongswan installed.
    """
    if os.geteuid() != 0:
        pytest.skip("This test requires root privileges.")
        
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
    setup_script = os.path.join(script_dir, 'setup_testbed.sh')
    verify_script = os.path.join(script_dir, 'verify_testbed.sh')
    cleanup_script = os.path.join(script_dir, 'cleanup_testbed.sh')

    try:
        # Setup testbed
        setup_result = subprocess.run([setup_script], capture_output=True, text=True)
        assert setup_result.returncode == 0, f"Setup failed:\n{setup_result.stderr}"

        # Verify testbed
        verify_result = subprocess.run([verify_script], capture_output=True, text=True)
        assert verify_result.returncode == 0, f"Verification failed:\n{verify_result.stderr}\n{verify_result.stdout}"
        assert "SUCCESS: Encrypted ESP/NAT-T traffic observed." in verify_result.stdout

    finally:
        # Cleanup testbed
        cleanup_result = subprocess.run([cleanup_script], capture_output=True, text=True)
        assert cleanup_result.returncode == 0, f"Cleanup failed:\n{cleanup_result.stderr}"
