import re

with open('backend/main.py', 'r') as f:
    content = f.read()

content = content.replace("from backend.models import ScenarioAnalysis", "from backend.models import ScenarioAnalysis, CaptureMetadata")
content = content.replace("@app.get(\"/api/scenarios\", response_model=Dict[str, str])", "@app.get(\"/api/scenarios\", response_model=List[CaptureMetadata])")

list_scenarios_new = """def list_scenarios():
    \"\"\"
    Returns the metadata for all available predefined captures.
    \"\"\"
    return [scenario.capture for scenario in SCENARIO_RESULTS.values()]"""

content = re.sub(r'def list_scenarios\(\):.*?return PCAP_INDEX', list_scenarios_new, content, flags=re.DOTALL)

with open('backend/main.py', 'w') as f:
    f.write(content)
