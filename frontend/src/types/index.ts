export interface TrafficFlow {
    id: string;
    duration_sec: number;
    packets: number;
    bytes: number;
    throughput_bps: number;
    avg_packet_size: number;
    classification: string;
    confidence: number;
    is_inferred: boolean;
}

export interface IPSecInfo {
    protocol: string;
    ike_version: string;
    encryption: string;
    integrity: string;
    dh_group: string;
    pfs: boolean;
    authentication: string;
    mode: string;
    ipv6: boolean;
    traffic_selectors: string;
}

export interface SecurityFinding {
    id: string;
    severity: string;
    category: string;
    title: string;
    description: string;
    recommendation: string;
    status: string;
    evidence: string[];
    assessment: string;
    remediation_config: string;
    remediation_rationale: string;
    remediation_validation: string;
    evidence_type: string;
}

export interface ReportMetadata {
    generated_at: string;
    author: string;
}


export interface CaptureMetadata {
    id: string;
    filename: string;
    display_name: string;
    file_size_bytes: number;
    capture_started_at: string;
    duration_seconds: number;
    packet_count: number;
    ip_packet_count: number;
    ipsec_packet_count: number;
    ipsec_coverage_percent: number;
    protocol: string;
    ip_version: string;
    interfaces: string[];
    source_type: string;
    analysis_status: string;
    analysis_timestamp: string;
    risk_level: string;
    ike_version: string;
    encryption: string;
    integrity: string;
    mode: string;
}

export interface TrafficTimelinePoint {
    timestamp: number;
    packets: number;
    bytes: number;
}

export interface ScenarioAnalysis {
    capture: CaptureMetadata;
    scenario_id: string;
    filename: string;
    packet_count: number;
    duration_sec: number;
    flow_count: number;
    bytes_total: number;
    security_score: number;
    risk_level: string;
    ipsec: IPSecInfo;
    traffic_flows: TrafficFlow[];
    traffic_timeline: TrafficTimelinePoint[];
    findings: SecurityFinding[];
    report_metadata: ReportMetadata;
}
