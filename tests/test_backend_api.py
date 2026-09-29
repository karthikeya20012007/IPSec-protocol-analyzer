import pytest
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app, CAPTURE_REGISTRY
from backend.data.scenarios import SCENARIO_RESULTS

client = TestClient(app)

# ==========================================
# Existing API Tests (preserved)
# ==========================================

def test_list_scenarios():
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(SCENARIO_RESULTS)
    assert "filename" in data[0]

def test_get_scenario_analysis():
    response = client.get("/api/analyze/S01")
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "S01"
    assert data["filename"] == "01-strong-gcm256.pcap"
    assert data["security_score"] == 95

def test_get_scenario_analysis_not_found():
    response = client.get("/api/analyze/UNKNOWN")
    assert response.status_code == 404

def test_upload_pcap_known_files():
    test_content = b"fake s01 content"
    h = hashlib.sha256(test_content).hexdigest()
    CAPTURE_REGISTRY[h] = {"scenario_id": "S01", "filename": "01-strong-gcm256.pcap"}
    files = {"file": ("01-strong-gcm256.pcap", test_content)}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "S01"
    assert data["security_score"] == 95

    test_content_s06 = b"fake s06 content"
    h6 = hashlib.sha256(test_content_s06).hexdigest()
    CAPTURE_REGISTRY[h6] = {"scenario_id": "S06", "filename": "06-weak-ikev1.pcap"}
    files = {"file": ("06-weak-ikev1.pcap", test_content_s06)}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "S06"
    assert data["risk_level"] == "HIGH"

    test_content_ex01 = b"fake ex01 content"
    hex01 = hashlib.sha256(test_content_ex01).hexdigest()
    CAPTURE_REGISTRY[hex01] = {"scenario_id": "EX01", "filename": "ikev2_s2s_ipsec_vpn_aes_gcm.pcapng"}
    files = {"file": ("ikev2_s2s_ipsec_vpn_aes_gcm.pcapng", test_content_ex01)}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["scenario_id"] == "EX01"
    assert data["capture"]["source_type"] == "EXTERNAL"
    assert data["packet_count"] == 12

def test_upload_pcap_unknown_file_error():
    files = {"file": ("unknown-capture.pcap", b"random garbage bytes")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 400
    data = response.json()
    assert "not part of the validated capture library" in data["detail"]


# ==========================================
# Remediation Patch Tests
# ==========================================

def test_s01_no_remediation():
    """S01 (strong config) should have no findings and no remediation."""
    s01 = SCENARIO_RESULTS["S01"]
    assert len(s01.findings) == 0

def test_s02_has_remediation_patch():
    """S02 (weak CBC/SHA-1) should have remediation patches for both findings."""
    s02 = SCENARIO_RESULTS["S02"]
    assert len(s02.findings) == 2
    for f in s02.findings:
        assert f.remediation_config != ""
        assert f.remediation_rationale != ""
        assert f.remediation_validation != ""

def test_s02_patch_contains_observed_old_value():
    """S02 patch must contain the actual observed old proposal."""
    s02 = SCENARIO_RESULTS["S02"]
    for f in s02.findings:
        assert "aes128-sha1" in f.remediation_config, \
            f"FIND {f.id}: patch must reference the observed aes128-sha1 proposal"

def test_s02_patch_contains_proposed_new_value():
    """S02 patch must contain the proposed new proposal."""
    s02 = SCENARIO_RESULTS["S02"]
    for f in s02.findings:
        assert "aes256gcm16" in f.remediation_config, \
            f"FIND {f.id}: patch must propose aes256gcm16"

def test_s03_no_remediation():
    """S03 (transport GCM) should have no findings."""
    s03 = SCENARIO_RESULTS["S03"]
    assert len(s03.findings) == 0

def test_s04_has_cbc_remediation():
    """S04 (CBC-256/DH-4096) should have a CBC modernization finding with patch."""
    s04 = SCENARIO_RESULTS["S04"]
    assert len(s04.findings) >= 1
    cbc_finding = s04.findings[0]
    assert cbc_finding.id == "FIND-010"
    assert cbc_finding.severity == "LOW"
    assert cbc_finding.remediation_config != ""
    assert "aes256-sha256-modp4096" in cbc_finding.remediation_config
    assert "aes256gcm16" in cbc_finding.remediation_config
    assert "modp4096" in cbc_finding.remediation_config
    assert cbc_finding.remediation_rationale != ""
    assert cbc_finding.remediation_validation != ""

def test_s05_pfs_remediation():
    """S05 (no PFS) should have targeted PFS remediation."""
    s05 = SCENARIO_RESULTS["S05"]
    assert len(s05.findings) == 2
    pfs_finding = s05.findings[0]
    assert pfs_finding.id == "FIND-003"
    assert "esp_proposals = aes256gcm16" in pfs_finding.remediation_config
    assert "ecp256" in pfs_finding.remediation_config
    assert pfs_finding.remediation_rationale != ""
    assert pfs_finding.remediation_validation != ""

def test_s06_has_modernization_remediation():
    """S06 (legacy IKE/3DES/MD5) should have 5 findings with complete remediation."""
    s06 = SCENARIO_RESULTS["S06"]
    assert len(s06.findings) == 5
    for f in s06.findings:
        assert f.remediation_config != "", f"FIND {f.id} must have remediation"
        assert f.remediation_rationale != "", f"FIND {f.id} must have rationale"
        assert f.remediation_validation != "", f"FIND {f.id} must have validation"

def test_s06_patch_contains_observed_3des():
    """S06 patches referencing IKE proposals must show the observed 3des-md5-modp1024."""
    s06 = SCENARIO_RESULTS["S06"]
    ike_findings = [f for f in s06.findings if "3des-md5-modp1024" in f.remediation_config]
    assert len(ike_findings) >= 3

def test_s06_patch_contains_proposed_modern():
    """S06 patches must propose modern aes256gcm16."""
    s06 = SCENARIO_RESULTS["S06"]
    for f in s06.findings:
        assert "aes256gcm16" in f.remediation_config, \
            f"FIND {f.id}: patch must propose modern cipher"

def test_ex01_no_remediation():
    """EX01 (external Wireshark capture) should have no findings."""
    ex01 = SCENARIO_RESULTS["EX01"]
    assert len(ex01.findings) == 0

def test_no_remediation_executes_anything():
    """Verify no remediation_config contains shell commands."""
    for scenario_id, scenario in SCENARIO_RESULTS.items():
        for f in scenario.findings:
            if f.remediation_config:
                assert "swanctl --load" not in f.remediation_config
                assert "systemctl" not in f.remediation_config
                assert "#!/" not in f.remediation_config

def test_all_capture_mappings_exist():
    """All expected scenario IDs must exist."""
    expected = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "EX01"]
    for sid in expected:
        assert sid in SCENARIO_RESULTS, f"Scenario {sid} must exist"

def test_s01_output_unchanged():
    """S01 core values must remain unchanged."""
    s01 = SCENARIO_RESULTS["S01"]
    assert s01.security_score == 95
    assert s01.risk_level == "LOW"
    assert s01.ipsec.encryption == "AES-256-GCM"
    assert s01.ipsec.ike_version == "IKEv2"

def test_s06_output_unchanged():
    """S06 core values must remain unchanged."""
    s06 = SCENARIO_RESULTS["S06"]
    assert s06.security_score == 42
    assert s06.risk_level == "HIGH"
    assert s06.ipsec.encryption == "3DES"
    assert s06.ipsec.ike_version == "IKEv1"
    assert s06.ipsec.integrity == "MD5"
    assert len(s06.findings) == 5

def test_remediation_has_file_path_comment():
    """Remediation configs should include a file path comment."""
    for scenario_id, scenario in SCENARIO_RESULTS.items():
        for f in scenario.findings:
            if f.remediation_config:
                assert "swanctl" in f.remediation_config.lower() or "conf" in f.remediation_config.lower(), \
                    f"{scenario_id}/{f.id}: remediation should reference config file"
