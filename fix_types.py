import re

with open('frontend/src/types/index.ts', 'r') as f:
    content = f.read()

new_types = """
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
}

"""

if "CaptureMetadata" not in content:
    content = content.replace("export interface TrafficTimelinePoint {", new_types + "export interface TrafficTimelinePoint {")

if "capture: CaptureMetadata" not in content:
    content = content.replace("export interface ScenarioAnalysis {", "export interface ScenarioAnalysis {\n    capture: CaptureMetadata;")

with open('frontend/src/types/index.ts', 'w') as f:
    f.write(content)
