from pydantic import BaseModel
from typing import List

class TrafficFlow(BaseModel):
    id: str
    duration_sec: float
    packets: int
    bytes: int
    throughput_bps: float
    avg_packet_size: int
    classification: str
    confidence: float
    is_inferred: bool

class IPSecInfo(BaseModel):
    protocol: str
    ike_version: str
    encryption: str
    integrity: str
    dh_group: str
    pfs: bool
    authentication: str
    mode: str
    ipv6: bool
    traffic_selectors: str

class SecurityFinding(BaseModel):
    id: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str
    title: str
    description: str
    recommendation: str
    status: str = "OPEN"
    evidence: list[str] = []
    assessment: str = ""
    remediation_config: str = ""
    remediation_rationale: str = ""
    remediation_validation: str = ""
    evidence_type: str = "OBSERVED"

class ReportMetadata(BaseModel):
    generated_at: str
    author: str


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
    risk_level: str
    ike_version: str
    encryption: str
    integrity: str
    mode: str

class TrafficTimelinePoint(BaseModel):
    timestamp: int
    packets: int
    bytes: int

class ScenarioAnalysis(BaseModel):
    capture: CaptureMetadata
    scenario_id: str
    filename: str
    packet_count: int
    duration_sec: float
    flow_count: int
    bytes_total: int
    security_score: int
    risk_level: str  # CRITICAL, HIGH, MEDIUM, LOW, SECURE
    ipsec: IPSecInfo
    traffic_flows: List[TrafficFlow]
    traffic_timeline: List[TrafficTimelinePoint]
    findings: List[SecurityFinding]
    report_metadata: ReportMetadata
