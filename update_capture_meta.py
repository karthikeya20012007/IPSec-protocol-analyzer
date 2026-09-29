import re

with open('backend/models.py', 'r') as f:
    content = f.read()

new_fields = """    analysis_status: str
    analysis_timestamp: str
    risk_level: str
    ike_version: str
    encryption: str
    integrity: str
    mode: str"""

content = content.replace("    analysis_status: str\n    analysis_timestamp: str", new_fields)

with open('backend/models.py', 'w') as f:
    f.write(content)

with open('frontend/src/types/index.ts', 'r') as f:
    content = f.read()

new_ts_fields = """    analysis_status: string;
    analysis_timestamp: string;
    risk_level: string;
    ike_version: string;
    encryption: string;
    integrity: string;
    mode: string;"""

content = content.replace("    analysis_status: string;\n    analysis_timestamp: string;", new_ts_fields)

with open('frontend/src/types/index.ts', 'w') as f:
    f.write(content)

# Update scenarios.py to pass these
with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

# We need to find the risk_level, ike_version etc. for each scenario and add them to CaptureMetadata
# Wait, they are passed as arguments to ScenarioAnalysis.
# Let's use regex to find them.

for sid in ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"]:
    block_match = re.search(rf'SCENARIO_RESULTS\["{sid}"\] = ScenarioAnalysis\((.*?)\)', content, re.DOTALL)
    if not block_match: continue
    block = block_match.group(1)
    
    risk_match = re.search(r'risk_level="([^"]+)"', block)
    ike_match = re.search(r'ike_version="([^"]+)"', block)
    enc_match = re.search(r'encryption="([^"]+)"', block)
    int_match = re.search(r'integrity="([^"]+)"', block)
    mode_match = re.search(r'mode="([^"]+)"', block)
    
    if not (risk_match and ike_match and enc_match and int_match and mode_match): continue
    
    new_args = f"""analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="{risk_match.group(1)}",
        ike_version="{ike_match.group(1)}",
        encryption="{enc_match.group(1)}",
        integrity="{int_match.group(1)}",
        mode="{mode_match.group(1)}"
    ),"""
    
    content = re.sub(rf'analysis_status="ANALYZED",\s+analysis_timestamp="2026-09-28T12:05:00Z"\s+\),', new_args, content, count=1)

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)
