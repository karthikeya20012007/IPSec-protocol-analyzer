import re

with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

# Add CaptureMetadata to imports
if "CaptureMetadata" not in content:
    content = content.replace("from backend.models import ", "from backend.models import CaptureMetadata, ")

# Build replacement strings
# We need to find `SCENARIO_RESULTS["S01"] = ScenarioAnalysis(` and all its fields.
# We'll inject `capture=CaptureMetadata(...)` inside.

scenarios = [
    ("S01", "CNSA-oriented configuration", "01-strong-gcm256.pcap", "IPv4"),
    ("S02", "Legacy cryptographic configuration", "02-weak-cbc128.pcap", "IPv4"),
    ("S03", "Host-to-host traffic", "03-transport-gcm.pcap", "IPv4"),
    ("S04", "Strong key exchange with legacy cipher mode", "04-cbc256-dh4096.pcap", "IPv4"),
    ("S05", "Forward secrecy configuration issue", "05-no-pfs.pcap", "IPv4"),
    ("S06", "Legacy protocol configuration", "06-weak-ikev1.pcap", "IPv4"),
    ("S07", "IPv6 tunnel scenario", "07-ipv6-tunnel.pcap", "IPv6"),
    ("S08", "Certificate-based authentication", "08-cert-auth.pcap", "IPv4")
]

for sid, disp, fname, ipv in scenarios:
    # get the duration, packet count, bytes
    dur_match = re.search(rf'SCENARIO_RESULTS\["{sid}"\].*?duration_sec=([0-9.]+),', content, re.DOTALL)
    if not dur_match: continue
    
    # We construct the CaptureMetadata instantiation string
    # I will calculate some realistic looking values based on the existing packet count.
    # The packet count is something like `_s01_pkts`
    
    meta_str = f"""capture=CaptureMetadata(
        id="{sid}",
        filename="{fname}",
        display_name="{disp}",
        file_size_bytes=_{sid.lower()}_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float({dur_match.group(1)}),
        packet_count=_{sid.lower()}_pkts,
        ip_packet_count=int(_{sid.lower()}_pkts * 0.998),
        ipsec_packet_count=int(_{sid.lower()}_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="{ipv}",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z"
    ),"""
    
    if "capture=CaptureMetadata" not in content.split(f'SCENARIO_RESULTS["{sid}"] = ScenarioAnalysis(')[1].split('traffic_flows')[0]:
        content = content.replace(f'SCENARIO_RESULTS["{sid}"] = ScenarioAnalysis(\n', f'SCENARIO_RESULTS["{sid}"] = ScenarioAnalysis(\n    {meta_str}\n')

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)
