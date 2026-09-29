import re

with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

# I will find each SCENARIO_RESULTS block and replace its CaptureMetadata
def replace_capture_meta(match):
    full_block = match.group(0)
    
    # Extract risk_level
    risk_match = re.search(r'risk_level="([^"]+)"', full_block)
    risk_level = risk_match.group(1) if risk_match else "UNKNOWN"
    
    # Extract IPSecInfo fields
    ike_match = re.search(r'ike_version="([^"]+)"', full_block)
    enc_match = re.search(r'encryption="([^"]+)"', full_block)
    int_match = re.search(r'integrity="([^"]+)"', full_block)
    mode_match = re.search(r'mode="([^"]+)"', full_block)
    
    ike_version = ike_match.group(1) if ike_match else "UNKNOWN"
    encryption = enc_match.group(1) if enc_match else "UNKNOWN"
    integrity = int_match.group(1) if int_match else "UNKNOWN"
    mode = mode_match.group(1) if mode_match else "UNKNOWN"
    
    # We find the end of CaptureMetadata
    # The CaptureMetadata ends with analysis_timestamp="2026-09-28T12:05:00Z"
    # We will append the missing fields right after it.
    
    new_capture_meta_fields = f""",
        risk_level="{risk_level}",
        ike_version="{ike_version}",
        encryption="{encryption}",
        integrity="{integrity}",
        mode="{mode}"
    )"""
    
    # Replace the closing parenthesis of CaptureMetadata
    # It looks like: analysis_timestamp="2026-09-28T12:05:00Z"\n    ),
    # We'll replace analysis_timestamp="..."\n    ) with analysis_timestamp="..." + our new fields
    
    new_block = re.sub(
        r'(analysis_timestamp="2026-09-28T12:05:00Z")\s*\),', 
        r'\1' + new_capture_meta_fields + ',', 
        full_block, 
        count=1
    )
    
    return new_block

# Run it for each scenario block
new_content = re.sub(r'SCENARIO_RESULTS\["S0[1-8]"\] = ScenarioAnalysis\(.*?\n\)', replace_capture_meta, content, flags=re.DOTALL)

with open('backend/data/scenarios.py', 'w') as f:
    f.write(new_content)

