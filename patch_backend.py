import re

SCENARIOS_PY = "backend/data/scenarios.py"

with open(SCENARIOS_PY, 'r') as f:
    content = f.read()

# Add EX01 mapping
if 'SCENARIO_RESULTS["EX01"]' not in content:
    ex01_def = """

# EX01: Wireshark External Validation Capture
SCENARIO_RESULTS["EX01"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="EX01",
        filename="ikev2_s2s_ipsec_vpn_aes_gcm.pcapng",
        display_name="Site-to-Site IKEv2 VPN with AES-256-GCM",
        file_size_bytes=10240,  # approximate
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=5.018,
        packet_count=12,
        ip_packet_count=12,
        ipsec_packet_count=8,
        ipsec_coverage_percent=66.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["external"],
        source_type="EXTERNAL",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="SECURE",
        ike_version="IKEv2",
        encryption="AES-GCM",
        integrity="16-octet ICV",
        mode="Tunnel"
    ),
    scenario_id="EX01",
    filename="ikev2_s2s_ipsec_vpn_aes_gcm.pcapng",
    packet_count=12,
    duration_sec=5.018,
    flow_count=2,
    bytes_total=1800,
    security_score=100,
    risk_level="SECURE",
    ipsec=IPSecInfo(
        protocol="ESP",
        ike_version="IKEv2",
        mode="Tunnel",
        encryption="AES-GCM",
        integrity="16-octet ICV",
        dh_group="Group 19 (256-bit ECP)",
        pfs=True,
        authentication="PSK",
        ipv6=False,
        traffic_selectors="10.0.0.1/32 === 10.0.0.2/32"
    ),
    traffic_flows=[
        TrafficFlow(id="ex01-ike", duration_sec=1.0, packets=4, bytes=800, throughput_bps=6400, avg_packet_size=200, classification="ISAKMP", confidence=1.0, is_inferred=False),
        TrafficFlow(id="ex01-esp", duration_sec=5.0, packets=8, bytes=1000, throughput_bps=1600, avg_packet_size=125, classification="ESP", confidence=1.0, is_inferred=False)
    ],
    traffic_timeline=[],
    findings=[],
    report_metadata=_REPORT_META
)
"""
    content += ex01_def

with open(SCENARIOS_PY, 'w') as f:
    f.write(content)

print("Added EX01 to scenarios.py")
