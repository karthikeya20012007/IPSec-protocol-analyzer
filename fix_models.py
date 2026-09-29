import re

with open('backend/models.py', 'r') as f:
    content = f.read()

new_models = """
class CaptureMetadata(BaseModel):
    id: str
    filename: str
    display_name: str
    file_size_bytes: int
    capture_started_at: str
    duration_seconds: float
    packet_count: int
    ip_packet_count: int
    ipsec_packet_count: int
    ipsec_coverage_percent: float
    protocol: str
    ip_version: str
    interfaces: List[str]
    source_type: str
    analysis_status: str
    analysis_timestamp: str

"""

if "CaptureMetadata" not in content:
    content = content.replace("class TrafficTimelinePoint(BaseModel):", new_models + "class TrafficTimelinePoint(BaseModel):")

# add capture: CaptureMetadata to ScenarioAnalysis
if "capture: CaptureMetadata" not in content:
    content = content.replace("class ScenarioAnalysis(BaseModel):", "class ScenarioAnalysis(BaseModel):\n    capture: CaptureMetadata")

with open('backend/models.py', 'w') as f:
    f.write(content)
