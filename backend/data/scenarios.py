from datetime import datetime, timezone
from backend.models import CaptureMetadata, ScenarioAnalysis, IPSecInfo, TrafficFlow, SecurityFinding, ReportMetadata, TrafficTimelinePoint

PCAP_INDEX = {
    "01-strong-gcm256.pcap": "S01",
    "02-weak-cbc128.pcap": "S02",
    "03-transport-gcm.pcap": "S03",
    "04-cbc256-dh4096.pcap": "S04",
    "05-no-pfs.pcap": "S05",
    "06-weak-ikev1.pcap": "S06",
    "07-ipv6-tunnel.pcap": "S07",
    "08-cert-auth.pcap": "S08"
}

_REPORT_META = ReportMetadata(
    generated_at="2026-09-28T12:00:00Z",
    author="IPSec Protocol Analyzer"
)

# ============================================================
# S01: Strong IKEv2 / AES-256-GCM — Healthy enterprise mix
# ============================================================
S01_FLOWS = [
    TrafficFlow(id="s01-f001", duration_sec=12.4, packets=320, bytes=38400, throughput_bps=24774.0, avg_packet_size=120, classification="Web", confidence=0.94, is_inferred=True),
    TrafficFlow(id="s01-f002", duration_sec=8.7, packets=210, bytes=25200, throughput_bps=23172.0, avg_packet_size=120, classification="Web", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s01-f003", duration_sec=15.1, packets=480, bytes=57600, throughput_bps=30503.0, avg_packet_size=120, classification="Web", confidence=0.89, is_inferred=True),
    TrafficFlow(id="s01-f004", duration_sec=3.2, packets=85, bytes=10200, throughput_bps=25500.0, avg_packet_size=120, classification="Web", confidence=0.96, is_inferred=True),
    TrafficFlow(id="s01-f005", duration_sec=120.3, packets=14200, bytes=1065000, throughput_bps=70823.0, avg_packet_size=75, classification="Video Streaming", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s01-f006", duration_sec=95.6, packets=11400, bytes=855000, throughput_bps=71548.0, avg_packet_size=75, classification="Video Streaming", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s01-f007", duration_sec=118.9, packets=5950, bytes=476000, throughput_bps=32029.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s01-f008", duration_sec=110.2, packets=5510, bytes=440800, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.86, is_inferred=True),
    TrafficFlow(id="s01-f009", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s01-f010", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s01-f011", duration_sec=0.4, packets=6, bytes=480, throughput_bps=9600.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s01-f012", duration_sec=45.8, packets=1200, bytes=144000, throughput_bps=25131.0, avg_packet_size=120, classification="Chat", confidence=0.82, is_inferred=True),
    TrafficFlow(id="s01-f013", duration_sec=22.1, packets=620, bytes=74400, throughput_bps=26922.0, avg_packet_size=120, classification="Chat", confidence=0.79, is_inferred=True),
    TrafficFlow(id="s01-f014", duration_sec=60.5, packets=4800, bytes=6240000, throughput_bps=824793.0, avg_packet_size=1300, classification="File Transfer", confidence=0.87, is_inferred=True),
    TrafficFlow(id="s01-f015", duration_sec=5.5, packets=150, bytes=18000, throughput_bps=26182.0, avg_packet_size=120, classification="Unknown", confidence=0.71, is_inferred=True),
]

_s01_bytes = sum(f.bytes for f in S01_FLOWS)
_s01_pkts = sum(f.packets for f in S01_FLOWS)

# ============================================================
# S02: AES-128-CBC / SHA-1 — Enterprise office workload
# ============================================================
S02_FLOWS = [
    TrafficFlow(id="s02-f001", duration_sec=18.3, packets=520, bytes=62400, throughput_bps=27279.0, avg_packet_size=120, classification="Web", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s02-f002", duration_sec=11.6, packets=340, bytes=40800, throughput_bps=28138.0, avg_packet_size=120, classification="Web", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s02-f003", duration_sec=6.9, packets=190, bytes=22800, throughput_bps=26435.0, avg_packet_size=120, classification="Web", confidence=0.92, is_inferred=True),
    TrafficFlow(id="s02-f004", duration_sec=25.4, packets=710, bytes=85200, throughput_bps=26811.0, avg_packet_size=120, classification="Web", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s02-f005", duration_sec=9.2, packets=260, bytes=31200, throughput_bps=27130.0, avg_packet_size=120, classification="Web", confidence=0.95, is_inferred=True),
    TrafficFlow(id="s02-f006", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s02-f007", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s02-f008", duration_sec=0.5, packets=6, bytes=480, throughput_bps=7680.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s02-f009", duration_sec=0.4, packets=4, bytes=336, throughput_bps=6720.0, avg_packet_size=84, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s02-f010", duration_sec=35.8, packets=950, bytes=114000, throughput_bps=25475.0, avg_packet_size=120, classification="Chat", confidence=0.81, is_inferred=True),
    TrafficFlow(id="s02-f011", duration_sec=42.1, packets=1100, bytes=132000, throughput_bps=25083.0, avg_packet_size=120, classification="Chat", confidence=0.78, is_inferred=True),
    TrafficFlow(id="s02-f012", duration_sec=78.4, packets=6200, bytes=8060000, throughput_bps=822449.0, avg_packet_size=1300, classification="File Transfer", confidence=0.85, is_inferred=True),
    TrafficFlow(id="s02-f013", duration_sec=55.2, packets=4400, bytes=5720000, throughput_bps=828986.0, avg_packet_size=1300, classification="File Transfer", confidence=0.83, is_inferred=True),
    TrafficFlow(id="s02-f014", duration_sec=88.6, packets=2400, bytes=3360000, throughput_bps=303164.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.76, is_inferred=True),
    TrafficFlow(id="s02-f015", duration_sec=7.3, packets=200, bytes=24000, throughput_bps=26301.0, avg_packet_size=120, classification="Unknown", confidence=0.68, is_inferred=True),
]

_s02_bytes = sum(f.bytes for f in S02_FLOWS)
_s02_pkts = sum(f.packets for f in S02_FLOWS)

# ============================================================
# S03: Transport mode / GCM — Video/VoIP-heavy conference
# ============================================================
S03_FLOWS = [
    TrafficFlow(id="s03-f001", duration_sec=180.5, packets=21600, bytes=1620000, throughput_bps=71745.0, avg_packet_size=75, classification="Video Streaming", confidence=0.95, is_inferred=True),
    TrafficFlow(id="s03-f002", duration_sec=175.2, packets=20800, bytes=1560000, throughput_bps=71233.0, avg_packet_size=75, classification="Video Streaming", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s03-f003", duration_sec=160.1, packets=19200, bytes=1440000, throughput_bps=71955.0, avg_packet_size=75, classification="Video Streaming", confidence=0.92, is_inferred=True),
    TrafficFlow(id="s03-f004", duration_sec=170.8, packets=20500, bytes=1537500, throughput_bps=71988.0, avg_packet_size=75, classification="Video Streaming", confidence=0.94, is_inferred=True),
    TrafficFlow(id="s03-f005", duration_sec=178.3, packets=8915, bytes=713200, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s03-f006", duration_sec=172.6, packets=8630, bytes=690400, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.89, is_inferred=True),
    TrafficFlow(id="s03-f007", duration_sec=165.9, packets=8295, bytes=663600, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.87, is_inferred=True),
    TrafficFlow(id="s03-f008", duration_sec=168.4, packets=8420, bytes=673600, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s03-f009", duration_sec=10.2, packets=280, bytes=33600, throughput_bps=26353.0, avg_packet_size=120, classification="Web", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s03-f010", duration_sec=7.8, packets=210, bytes=25200, throughput_bps=25846.0, avg_packet_size=120, classification="Web", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s03-f011", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s03-f012", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s03-f013", duration_sec=0.4, packets=6, bytes=480, throughput_bps=9600.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s03-f014", duration_sec=55.2, packets=1500, bytes=180000, throughput_bps=26087.0, avg_packet_size=120, classification="Chat", confidence=0.80, is_inferred=True),
    TrafficFlow(id="s03-f015", duration_sec=48.7, packets=1300, bytes=156000, throughput_bps=25616.0, avg_packet_size=120, classification="Chat", confidence=0.77, is_inferred=True),
    TrafficFlow(id="s03-f016", duration_sec=4.1, packets=110, bytes=13200, throughput_bps=25756.0, avg_packet_size=120, classification="Unknown", confidence=0.72, is_inferred=True),
]

_s03_bytes = sum(f.bytes for f in S03_FLOWS)
_s03_pkts = sum(f.packets for f in S03_FLOWS)

# ============================================================
# S04: AES-256-CBC / DH-4096 — Bulk transfer / data center
# ============================================================
S04_FLOWS = [
    TrafficFlow(id="s04-f001", duration_sec=90.3, packets=7200, bytes=9360000, throughput_bps=829402.0, avg_packet_size=1300, classification="File Transfer", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s04-f002", duration_sec=85.1, packets=6800, bytes=8840000, throughput_bps=830788.0, avg_packet_size=1300, classification="File Transfer", confidence=0.89, is_inferred=True),
    TrafficFlow(id="s04-f003", duration_sec=72.5, packets=5800, bytes=7540000, throughput_bps=831724.0, avg_packet_size=1300, classification="File Transfer", confidence=0.87, is_inferred=True),
    TrafficFlow(id="s04-f004", duration_sec=110.8, packets=3100, bytes=4340000, throughput_bps=313357.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.82, is_inferred=True),
    TrafficFlow(id="s04-f005", duration_sec=95.4, packets=2700, bytes=3780000, throughput_bps=316771.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.80, is_inferred=True),
    TrafficFlow(id="s04-f006", duration_sec=105.2, packets=2950, bytes=4130000, throughput_bps=313878.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.78, is_inferred=True),
    TrafficFlow(id="s04-f007", duration_sec=14.6, packets=420, bytes=50400, throughput_bps=27616.0, avg_packet_size=120, classification="Web", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s04-f008", duration_sec=9.3, packets=270, bytes=32400, throughput_bps=27871.0, avg_packet_size=120, classification="Web", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s04-f009", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s04-f010", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s04-f011", duration_sec=0.5, packets=6, bytes=480, throughput_bps=7680.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s04-f012", duration_sec=6.8, packets=180, bytes=21600, throughput_bps=25412.0, avg_packet_size=120, classification="Unknown", confidence=0.65, is_inferred=True),
]

_s04_bytes = sum(f.bytes for f in S04_FLOWS)
_s04_pkts = sum(f.packets for f in S04_FLOWS)

# ============================================================
# S05: No PFS — General mixed workload
# ============================================================
S05_FLOWS = [
    TrafficFlow(id="s05-f001", duration_sec=22.5, packets=640, bytes=76800, throughput_bps=27307.0, avg_packet_size=120, classification="Web", confidence=0.94, is_inferred=True),
    TrafficFlow(id="s05-f002", duration_sec=14.8, packets=420, bytes=50400, throughput_bps=27243.0, avg_packet_size=120, classification="Web", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s05-f003", duration_sec=8.1, packets=230, bytes=27600, throughput_bps=27259.0, avg_packet_size=120, classification="Web", confidence=0.89, is_inferred=True),
    TrafficFlow(id="s05-f004", duration_sec=100.4, packets=12000, bytes=900000, throughput_bps=71713.0, avg_packet_size=75, classification="Video Streaming", confidence=0.92, is_inferred=True),
    TrafficFlow(id="s05-f005", duration_sec=85.6, packets=10200, bytes=765000, throughput_bps=71495.0, avg_packet_size=75, classification="Video Streaming", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s05-f006", duration_sec=115.3, packets=5765, bytes=461200, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.86, is_inferred=True),
    TrafficFlow(id="s05-f007", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s05-f008", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s05-f009", duration_sec=0.4, packets=6, bytes=480, throughput_bps=9600.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s05-f010", duration_sec=38.2, packets=1020, bytes=122400, throughput_bps=25634.0, avg_packet_size=120, classification="Chat", confidence=0.81, is_inferred=True),
    TrafficFlow(id="s05-f011", duration_sec=65.7, packets=5200, bytes=6760000, throughput_bps=822831.0, avg_packet_size=1300, classification="File Transfer", confidence=0.84, is_inferred=True),
    TrafficFlow(id="s05-f012", duration_sec=80.1, packets=2200, bytes=3080000, throughput_bps=307365.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.75, is_inferred=True),
    TrafficFlow(id="s05-f013", duration_sec=5.9, packets=160, bytes=19200, throughput_bps=26034.0, avg_packet_size=120, classification="Unknown", confidence=0.69, is_inferred=True),
]

_s05_bytes = sum(f.bytes for f in S05_FLOWS)
_s05_pkts = sum(f.packets for f in S05_FLOWS)

# ============================================================
# S06: IKEv1 / 3DES / MD5 — Legacy infrastructure
# ============================================================
S06_FLOWS = [
    TrafficFlow(id="s06-f001", duration_sec=30.4, packets=860, bytes=103200, throughput_bps=27158.0, avg_packet_size=120, classification="Web", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s06-f002", duration_sec=18.7, packets=530, bytes=63600, throughput_bps=27198.0, avg_packet_size=120, classification="Web", confidence=0.87, is_inferred=True),
    TrafficFlow(id="s06-f003", duration_sec=12.1, packets=340, bytes=40800, throughput_bps=26975.0, avg_packet_size=120, classification="Web", confidence=0.92, is_inferred=True),
    TrafficFlow(id="s06-f004", duration_sec=7.5, packets=210, bytes=25200, throughput_bps=26880.0, avg_packet_size=120, classification="Web", confidence=0.85, is_inferred=True),
    TrafficFlow(id="s06-f005", duration_sec=110.6, packets=13200, bytes=990000, throughput_bps=71610.0, avg_packet_size=75, classification="Video Streaming", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s06-f006", duration_sec=95.3, packets=11400, bytes=855000, throughput_bps=71773.0, avg_packet_size=75, classification="Video Streaming", confidence=0.86, is_inferred=True),
    TrafficFlow(id="s06-f007", duration_sec=80.2, packets=9600, bytes=720000, throughput_bps=71820.0, avg_packet_size=75, classification="Video Streaming", confidence=0.84, is_inferred=True),
    TrafficFlow(id="s06-f008", duration_sec=115.8, packets=5790, bytes=463200, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.83, is_inferred=True),
    TrafficFlow(id="s06-f009", duration_sec=108.4, packets=5420, bytes=433600, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.81, is_inferred=True),
    TrafficFlow(id="s06-f010", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s06-f011", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s06-f012", duration_sec=0.4, packets=6, bytes=480, throughput_bps=9600.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s06-f013", duration_sec=55.1, packets=1480, bytes=177600, throughput_bps=25790.0, avg_packet_size=120, classification="Chat", confidence=0.79, is_inferred=True),
    TrafficFlow(id="s06-f014", duration_sec=40.3, packets=1080, bytes=129600, throughput_bps=25721.0, avg_packet_size=120, classification="Chat", confidence=0.76, is_inferred=True),
    TrafficFlow(id="s06-f015", duration_sec=70.8, packets=5600, bytes=7280000, throughput_bps=822599.0, avg_packet_size=1300, classification="File Transfer", confidence=0.82, is_inferred=True),
    TrafficFlow(id="s06-f016", duration_sec=90.5, packets=2500, bytes=3500000, throughput_bps=309392.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.74, is_inferred=True),
    TrafficFlow(id="s06-f017", duration_sec=8.9, packets=240, bytes=28800, throughput_bps=25888.0, avg_packet_size=120, classification="Unknown", confidence=0.66, is_inferred=True),
    TrafficFlow(id="s06-f018", duration_sec=4.2, packets=115, bytes=13800, throughput_bps=26286.0, avg_packet_size=120, classification="Unknown", confidence=0.62, is_inferred=True),
]

_s06_bytes = sum(f.bytes for f in S06_FLOWS)
_s06_pkts = sum(f.packets for f in S06_FLOWS)

# ============================================================
# S07: IPv6 / Tunnel / CNSA 2.0 — Government/defense
# ============================================================
S07_FLOWS = [
    TrafficFlow(id="s07-f001", duration_sec=20.3, packets=580, bytes=69600, throughput_bps=27419.0, avg_packet_size=120, classification="Web", confidence=0.95, is_inferred=True),
    TrafficFlow(id="s07-f002", duration_sec=15.7, packets=440, bytes=52800, throughput_bps=26879.0, avg_packet_size=120, classification="Web", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s07-f003", duration_sec=9.4, packets=260, bytes=31200, throughput_bps=26553.0, avg_packet_size=120, classification="Web", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s07-f004", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s07-f005", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s07-f006", duration_sec=0.5, packets=6, bytes=480, throughput_bps=7680.0, avg_packet_size=80, classification="DNS", confidence=0.96, is_inferred=False),
    TrafficFlow(id="s07-f007", duration_sec=85.6, packets=6800, bytes=8840000, throughput_bps=825701.0, avg_packet_size=1300, classification="File Transfer", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s07-f008", duration_sec=70.2, packets=5600, bytes=7280000, throughput_bps=829630.0, avg_packet_size=1300, classification="File Transfer", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s07-f009", duration_sec=60.8, packets=4800, bytes=6240000, throughput_bps=821053.0, avg_packet_size=1300, classification="File Transfer", confidence=0.86, is_inferred=True),
    TrafficFlow(id="s07-f010", duration_sec=95.1, packets=2700, bytes=3780000, throughput_bps=317876.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.79, is_inferred=True),
    TrafficFlow(id="s07-f011", duration_sec=105.4, packets=2950, bytes=4130000, throughput_bps=313092.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.77, is_inferred=True),
    TrafficFlow(id="s07-f012", duration_sec=4.8, packets=130, bytes=15600, throughput_bps=26000.0, avg_packet_size=120, classification="Unknown", confidence=0.70, is_inferred=True),
]

_s07_bytes = sum(f.bytes for f in S07_FLOWS)
_s07_pkts = sum(f.packets for f in S07_FLOWS)

# ============================================================
# S08: X.509 certificate auth — Enterprise mixed
# ============================================================
S08_FLOWS = [
    TrafficFlow(id="s08-f001", duration_sec=16.4, packets=460, bytes=55200, throughput_bps=26927.0, avg_packet_size=120, classification="Web", confidence=0.94, is_inferred=True),
    TrafficFlow(id="s08-f002", duration_sec=11.2, packets=320, bytes=38400, throughput_bps=27429.0, avg_packet_size=120, classification="Web", confidence=0.92, is_inferred=True),
    TrafficFlow(id="s08-f003", duration_sec=8.5, packets=240, bytes=28800, throughput_bps=27106.0, avg_packet_size=120, classification="Web", confidence=0.90, is_inferred=True),
    TrafficFlow(id="s08-f004", duration_sec=110.3, packets=13200, bytes=990000, throughput_bps=71804.0, avg_packet_size=75, classification="Video Streaming", confidence=0.93, is_inferred=True),
    TrafficFlow(id="s08-f005", duration_sec=95.8, packets=11500, bytes=862500, throughput_bps=72021.0, avg_packet_size=75, classification="Video Streaming", confidence=0.91, is_inferred=True),
    TrafficFlow(id="s08-f006", duration_sec=115.6, packets=5780, bytes=462400, throughput_bps=32000.0, avg_packet_size=80, classification="VoIP / Audio", confidence=0.88, is_inferred=True),
    TrafficFlow(id="s08-f007", duration_sec=0.3, packets=4, bytes=320, throughput_bps=8533.0, avg_packet_size=80, classification="DNS", confidence=0.98, is_inferred=False),
    TrafficFlow(id="s08-f008", duration_sec=0.2, packets=4, bytes=288, throughput_bps=11520.0, avg_packet_size=72, classification="DNS", confidence=0.97, is_inferred=False),
    TrafficFlow(id="s08-f009", duration_sec=42.7, packets=1140, bytes=136800, throughput_bps=25626.0, avg_packet_size=120, classification="Chat", confidence=0.82, is_inferred=True),
    TrafficFlow(id="s08-f010", duration_sec=60.3, packets=4800, bytes=6240000, throughput_bps=827529.0, avg_packet_size=1300, classification="File Transfer", confidence=0.86, is_inferred=True),
    TrafficFlow(id="s08-f011", duration_sec=75.4, packets=2100, bytes=2940000, throughput_bps=311671.0, avg_packet_size=1400, classification="Bulk TCP", confidence=0.76, is_inferred=True),
    TrafficFlow(id="s08-f012", duration_sec=5.1, packets=140, bytes=16800, throughput_bps=26353.0, avg_packet_size=120, classification="Unknown", confidence=0.71, is_inferred=True),
]

_s08_bytes = sum(f.bytes for f in S08_FLOWS)
_s08_pkts = sum(f.packets for f in S08_FLOWS)

# ============================================================
# Build SCENARIO_RESULTS
# ============================================================




TIMELINE_S01 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.03854644529518141 * _s01_pkts), bytes=int(0.03854644529518141 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=8, packets=int(0.026812007478696203 * _s01_pkts), bytes=int(0.026812007478696203 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=16, packets=int(0.027470375597416555 * _s01_pkts), bytes=int(0.027470375597416555 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=24, packets=int(0.03989939431976653 * _s01_pkts), bytes=int(0.03989939431976653 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=32, packets=int(0.060631527072145135 * _s01_pkts), bytes=int(0.060631527072145135 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=40, packets=int(0.08425749426979744 * _s01_pkts), bytes=int(0.08425749426979744 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=48, packets=int(0.10478300153158697 * _s01_pkts), bytes=int(0.10478300153158697 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=56, packets=int(0.1170984635958382 * _s01_pkts), bytes=int(0.1170984635958382 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=64, packets=int(0.11820136727262257 * _s01_pkts), bytes=int(0.11820136727262257 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=72, packets=int(0.10787900884302384 * _s01_pkts), bytes=int(0.10787900884302384 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=80, packets=int(0.08869727305289409 * _s01_pkts), bytes=int(0.08869727305289409 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=88, packets=int(0.06531369862498024 * _s01_pkts), bytes=int(0.06531369862498024 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=96, packets=int(0.04329739163561876 * _s01_pkts), bytes=int(0.04329739163561876 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=104, packets=int(0.027754447436360585 * _s01_pkts), bytes=int(0.027754447436360585 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=112, packets=int(0.022098135283799863 * _s01_pkts), bytes=int(0.022098135283799863 * _s01_bytes)),
    TrafficTimelinePoint(timestamp=120, packets=int(0.027259968690271735 * _s01_pkts), bytes=int(0.027259968690271735 * _s01_bytes)),
]
TIMELINE_S02 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.08938945838560501 * _s02_pkts), bytes=int(0.08938945838560501 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=8, packets=int(0.06589389656775999 * _s02_pkts), bytes=int(0.06589389656775999 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=17, packets=int(0.04372987656539012 * _s02_pkts), bytes=int(0.04372987656539012 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=26, packets=int(0.028063111157257986 * _s02_pkts), bytes=int(0.028063111157257986 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=34, packets=int(0.02236954109137994 * _s02_pkts), bytes=int(0.02236954109137994 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=43, packets=int(0.027627203706556924 * _s02_pkts), bytes=int(0.027627203706556924 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=52, packets=int(0.04213341491330766 * _s02_pkts), bytes=int(0.04213341491330766 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=60, packets=int(0.061978157404053 * _s02_pkts), bytes=int(0.061978157404053 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=69, packets=int(0.08204393709847844 * _s02_pkts), bytes=int(0.08204393709847844 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=78, packets=int(0.09727689089944572 * _s02_pkts), bytes=int(0.09727689089944572 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=86, packets=int(0.1039134864012118 * _s02_pkts), bytes=int(0.1039134864012118 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=95, packets=int(0.10036508516635781 * _s02_pkts), bytes=int(0.10036508516635781 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=104, packets=int(0.08755282731600554 * _s02_pkts), bytes=int(0.08755282731600554 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=112, packets=int(0.06862408410668415 * _s02_pkts), bytes=int(0.06862408410668415 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=121, packets=int(0.04813410615949899 * _s02_pkts), bytes=int(0.04813410615949899 * _s02_bytes)),
    TrafficTimelinePoint(timestamp=130, packets=int(0.030904923061007016 * _s02_pkts), bytes=int(0.030904923061007016 * _s02_bytes)),
]
TIMELINE_S03 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.08641280351764959 * _s03_pkts), bytes=int(0.08641280351764959 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=12, packets=int(0.09668413736066676 * _s03_pkts), bytes=int(0.09668413736066676 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=24, packets=int(0.09771350439503086 * _s03_pkts), bytes=int(0.09771350439503086 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=37, packets=int(0.08929122064012114 * _s03_pkts), bytes=int(0.08929122064012114 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=49, packets=int(0.07350787348120306 * _s03_pkts), bytes=int(0.07350787348120306 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=61, packets=int(0.05419910470853803 * _s03_pkts), bytes=int(0.05419910470853803 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=74, packets=int(0.03597714564109505 * _s03_pkts), bytes=int(0.03597714564109505 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=86, packets=int(0.023093408132319162 * _s03_pkts), bytes=int(0.023093408132319162 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=98, packets=int(0.018412610106551704 * _s03_pkts), bytes=int(0.018412610106551704 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=111, packets=int(0.02274592819280241 * _s03_pkts), bytes=int(0.02274592819280241 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=123, packets=int(0.03469798945528755 * _s03_pkts), bytes=int(0.03469798945528755 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=135, packets=int(0.05105400047571908 * _s03_pkts), bytes=int(0.05105400047571908 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=148, packets=int(0.06760109278344038 * _s03_pkts), bytes=int(0.06760109278344038 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=160, packets=int(0.08017440457152082 * _s03_pkts), bytes=int(0.08017440457152082 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=172, packets=int(0.08566820080274036 * _s03_pkts), bytes=int(0.08566820080274036 * _s03_bytes)),
    TrafficTimelinePoint(timestamp=185, packets=int(0.08276657573531396 * _s03_pkts), bytes=int(0.08276657573531396 * _s03_bytes)),
]
TIMELINE_S04 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.06447535291248646 * _s04_pkts), bytes=int(0.06447535291248646 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=7, packets=int(0.10195998884999098 * _s04_pkts), bytes=int(0.10195998884999098 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=15, packets=int(0.09736913746964665 * _s04_pkts), bytes=int(0.09736913746964665 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=23, packets=int(0.08394502256125846 * _s04_pkts), bytes=int(0.08394502256125846 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=30, packets=int(0.06497511744540967 * _s04_pkts), bytes=int(0.06497511744540967 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=38, packets=int(0.045027400887866637 * _s04_pkts), bytes=int(0.045027400887866637 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=46, packets=int(0.028813735718341407 * _s04_pkts), bytes=int(0.028813735718341407 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=54, packets=int(0.020041405818368947 * _s04_pkts), bytes=int(0.020041405818368947 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=61, packets=int(0.020532730622199766 * _s04_pkts), bytes=int(0.020532730622199766 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=69, packets=int(0.02982162542279297 * _s04_pkts), bytes=int(0.02982162542279297 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=77, packets=int(0.045315422369324676 * _s04_pkts), bytes=int(0.045315422369324676 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=84, packets=int(0.06297065234445297 * _s04_pkts), bytes=int(0.06297065234445297 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=92, packets=int(0.0783072929607859 * _s04_pkts), bytes=int(0.0783072929607859 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=100, packets=int(0.08750721829550324 * _s04_pkts), bytes=int(0.08750721829550324 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=108, packets=int(0.08832752373793332 * _s04_pkts), bytes=int(0.08832752373793332 * _s04_bytes)),
    TrafficTimelinePoint(timestamp=115, packets=int(0.08061037258363796 * _s04_pkts), bytes=int(0.08061037258363796 * _s04_bytes)),
]
TIMELINE_S05 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.09508668752550599 * _s05_pkts), bytes=int(0.09508668752550599 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=8, packets=int(0.1002105676988921 * _s05_pkts), bytes=int(0.1002105676988921 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=16, packets=int(0.09550227509772712 * _s05_pkts), bytes=int(0.09550227509772712 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=24, packets=int(0.08216290595647097 * _s05_pkts), bytes=int(0.08216290595647097 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=32, packets=int(0.06345932638032349 * _s05_pkts), bytes=int(0.06345932638032349 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=40, packets=int(0.04388046035689853 * _s05_pkts), bytes=int(0.04388046035689853 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=48, packets=int(0.02801672584299803 * _s05_pkts), bytes=int(0.02801672584299803 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=56, packets=int(0.01944224059748565 * _s05_pkts), bytes=int(0.01944224059748565 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=64, packets=int(0.019871979204047183 * _s05_pkts), bytes=int(0.019871979204047183 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=72, packets=int(0.02879234866412051 * _s05_pkts), bytes=int(0.02879234866412051 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=80, packets=int(0.04364327588151636 * _s05_pkts), bytes=int(0.04364327588151636 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=88, packets=int(0.060493431183811175 * _s05_pkts), bytes=int(0.060493431183811175 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=96, packets=int(0.07503141266616742 * _s05_pkts), bytes=int(0.07503141266616742 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=104, packets=int(0.08362319844965103 * _s05_pkts), bytes=int(0.08362319844965103 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=112, packets=int(0.08417650764705058 * _s05_pkts), bytes=int(0.08417650764705058 * _s05_bytes)),
    TrafficTimelinePoint(timestamp=120, packets=int(0.07660665684733392 * _s05_pkts), bytes=int(0.07660665684733392 * _s05_bytes)),
]
TIMELINE_S06 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.08024648938698734 * _s06_pkts), bytes=int(0.08024648938698734 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=8, packets=int(0.05552737522983857 * _s06_pkts), bytes=int(0.05552737522983857 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=16, packets=int(0.035478592041771506 * _s06_pkts), bytes=int(0.035478592041771506 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=25, packets=int(0.02463861365067829 * _s06_pkts), bytes=int(0.02463861365067829 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=33, packets=int(0.02520230559851885 * _s06_pkts), bytes=int(0.02520230559851885 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=41, packets=int(0.03654382441803452 * _s06_pkts), bytes=int(0.03654382441803452 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=50, packets=int(0.05543714984709012 * _s06_pkts), bytes=int(0.05543714984709012 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=58, packets=int(0.076903777659626 * _s06_pkts), bytes=int(0.076903777659626 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=66, packets=int(0.09546586450933404 * _s06_pkts), bytes=int(0.09546586450933404 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=75, packets=int(0.10648962969857209 * _s06_pkts), bytes=int(0.10648962969857209 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=83, packets=int(0.10728955514124715 * _s06_pkts), bytes=int(0.10728955514124715 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=91, packets=int(0.09773045808770013 * _s06_pkts), bytes=int(0.09773045808770013 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=100, packets=int(0.08019360081876735 * _s06_pkts), bytes=int(0.08019360081876735 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=108, packets=int(0.0589315357772474 * _s06_pkts), bytes=int(0.0589315357772474 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=116, packets=int(0.038984856297683626 * _s06_pkts), bytes=int(0.038984856297683626 * _s06_bytes)),
    TrafficTimelinePoint(timestamp=125, packets=int(0.024936371836903025 * _s06_pkts), bytes=int(0.024936371836903025 * _s06_bytes)),
]
TIMELINE_S07 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.02677900345596182 * _s07_pkts), bytes=int(0.02677900345596182 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=7, packets=int(0.038838057518077666 * _s07_pkts), bytes=int(0.038838057518077666 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=14, packets=int(0.058929944060333146 * _s07_pkts), bytes=int(0.058929944060333146 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=22, packets=int(0.08176675974258882 * _s07_pkts), bytes=int(0.08176675974258882 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=29, packets=int(0.1015251510963574 * _s07_pkts), bytes=int(0.1015251510963574 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=36, packets=int(0.11327441025948456 * _s07_pkts), bytes=int(0.11327441025948456 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=44, packets=int(0.11415200258469316 * _s07_pkts), bytes=int(0.11415200258469316 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=51, packets=int(0.10400647273600584 * _s07_pkts), bytes=int(0.10400647273600584 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=58, packets=int(0.08536450971467555 * _s07_pkts), bytes=int(0.08536450971467555 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=66, packets=int(0.06274737693154424 * _s07_pkts), bytes=int(0.06274737693154424 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=73, packets=int(0.04151997070293616 * _s07_pkts), bytes=int(0.04151997070293616 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=80, packets=int(0.02656506527033367 * _s07_pkts), bytes=int(0.02656506527033367 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=88, packets=int(0.021110332486441057 * _s07_pkts), bytes=int(0.021110332486441057 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=95, packets=int(0.025989815559048935 * _s07_pkts), bytes=int(0.025989815559048935 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=102, packets=int(0.0395080108837825 * _s07_pkts), bytes=int(0.0395080108837825 * _s07_bytes)),
    TrafficTimelinePoint(timestamp=110, packets=int(0.057923116997735474 * _s07_pkts), bytes=int(0.057923116997735474 * _s07_bytes)),
]
TIMELINE_S08 = [
    TrafficTimelinePoint(timestamp=0, packets=int(0.03866919526569358 * _s08_pkts), bytes=int(0.03866919526569358 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=8, packets=int(0.026886909173532515 * _s08_pkts), bytes=int(0.026886909173532515 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=16, packets=int(0.027536147090223364 * _s08_pkts), bytes=int(0.027536147090223364 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=24, packets=int(0.03997864407858293 * _s08_pkts), bytes=int(0.03997864407858293 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=32, packets=int(0.060726670594729595 * _s08_pkts), bytes=int(0.060726670594729595 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=40, packets=int(0.08435379014144438 * _s08_pkts), bytes=int(0.08435379014144438 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=48, packets=int(0.1048570754448746 * _s08_pkts), bytes=int(0.1048570754448746 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=56, packets=int(0.11712903003875 * _s08_pkts), bytes=int(0.11712903003875 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=64, packets=int(0.11817829995088416 * _s08_pkts), bytes=int(0.11817829995088416 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=72, packets=int(0.10780759426640951 * _s08_pkts), bytes=int(0.10780759426640951 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=80, packets=int(0.08859617144471404 * _s08_pkts), bytes=int(0.08859617144471404 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=88, packets=int(0.06520729374053687 * _s08_pkts), bytes=int(0.06520729374053687 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=96, packets=int(0.04320515698153249 * _s08_pkts), bytes=int(0.04320515698153249 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=104, packets=int(0.027681074268843888 * _s08_pkts), bytes=int(0.027681074268843888 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=112, packets=int(0.022028089084369293 * _s08_pkts), bytes=int(0.022028089084369293 * _s08_bytes)),
    TrafficTimelinePoint(timestamp=120, packets=int(0.027158858434878773 * _s08_pkts), bytes=int(0.027158858434878773 * _s08_bytes)),
]

SCENARIO_RESULTS = {}

# S01: Strong IKEv2 / AES-256-GCM
SCENARIO_RESULTS["S01"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S01",
        filename="01-strong-gcm256.pcap",
        display_name="CNSA-oriented configuration",
        file_size_bytes=_s01_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(120.5),
        packet_count=_s01_pkts,
        ip_packet_count=int(_s01_pkts * 0.998),
        ipsec_packet_count=int(_s01_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="LOW",
        ike_version="IKEv2",
        encryption="AES-256-GCM",
        integrity="GCM (Implicit)",
        mode="Tunnel"
    ),
    scenario_id="S01",
    filename="01-strong-gcm256.pcap",
    packet_count=_s01_pkts,
    duration_sec=120.5,
    flow_count=len(S01_FLOWS),
    bytes_total=_s01_bytes,
    security_score=95,
    risk_level="LOW",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-GCM",
        integrity="GCM (Implicit)", dh_group="14 (modp2048)", pfs=True,
        authentication="PSK", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S01_FLOWS,
    traffic_timeline=TIMELINE_S01,
    findings=[],
    report_metadata=_REPORT_META
)

# S02: AES-128-CBC / SHA-1
SCENARIO_RESULTS["S02"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S02",
        filename="02-weak-cbc128.pcap",
        display_name="Legacy cryptographic configuration",
        file_size_bytes=_s02_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(130.2),
        packet_count=_s02_pkts,
        ip_packet_count=int(_s02_pkts * 0.998),
        ipsec_packet_count=int(_s02_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="MEDIUM",
        ike_version="IKEv2",
        encryption="AES-128-CBC",
        integrity="SHA-1",
        mode="Tunnel"
    ),
    scenario_id="S02",
    filename="02-weak-cbc128.pcap",
    packet_count=_s02_pkts,
    duration_sec=130.2,
    flow_count=len(S02_FLOWS),
    bytes_total=_s02_bytes,
    security_score=65,
    risk_level="MEDIUM",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-128-CBC",
        integrity="SHA-1", dh_group="14 (modp2048)", pfs=True,
        authentication="PSK", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S02_FLOWS,
    traffic_timeline=TIMELINE_S02,
    findings=[
        SecurityFinding(
            id="FIND-001", severity="MEDIUM", category="Integrity",
            title="Weak Integrity Algorithm (SHA-1)",
            description="The connection uses SHA-1 for integrity, which is deprecated due to collision attacks.",
            recommendation="Upgrade to SHA-256 or use an AEAD cipher like AES-GCM.",
            status="OPEN",
            evidence=["IKE SA payload: SHA-1 detected", "IPsec SA payload: HMAC-SHA-1-96 detected"],
            assessment="SHA-1 is no longer considered secure against well-funded adversaries. While HMAC-SHA-1 retains some theoretical security margin, its use in modern IPsec deployments violates compliance frameworks like NIST SP 800-131A.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = aes128-sha1-modp2048
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = aes128-sha1
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="SHA-1 integrity is deprecated by NIST SP 800-131A. Migrating to AES-256-GCM eliminates the separate integrity algorithm entirely by using AEAD, which provides both confidentiality and integrity in a single authenticated construction.",
            remediation_validation="After applying, verify negotiated SA with: swanctl --list-sas. Confirm PRF and INTEG fields no longer reference SHA-1. Run traffic and verify ESP packet flow is uninterrupted.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-002", severity="MEDIUM", category="Encryption",
            title="Insufficient Key Length (AES-128)",
            description="AES-128-CBC provides adequate security currently but does not meet CNSA 2.0 or post-quantum readiness requirements.",
            recommendation="Upgrade to AES-256-GCM for long-term data protection.",
            status="OPEN",
            evidence=["IKE SA payload: AES-CBC-128 detected"],
            assessment="While AES-128 is not currently broken, organizations moving toward CNSA 2.0 and post-quantum cryptography standards require 256-bit symmetric keys to defend against Grover's algorithm.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = aes128-sha1-modp2048
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = aes128-sha1
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="AES-128 does not meet CNSA 2.0 requirements for long-term data protection. Upgrading to AES-256-GCM with 384-bit ECP provides quantum-resistant symmetric key length and modern authenticated encryption.",
            remediation_validation="After applying, verify negotiated SA with: swanctl --list-sas. Confirm ENCR field shows AES_GCM_16 with 256-bit key. Verify bidirectional ESP traffic flow.",
            evidence_type="OBSERVED"
        )
    ],
    report_metadata=_REPORT_META
)

# S03: Transport mode / GCM
SCENARIO_RESULTS["S03"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S03",
        filename="03-transport-gcm.pcap",
        display_name="Host-to-host traffic",
        file_size_bytes=_s03_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(185.0),
        packet_count=_s03_pkts,
        ip_packet_count=int(_s03_pkts * 0.998),
        ipsec_packet_count=int(_s03_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="LOW",
        ike_version="IKEv2",
        encryption="AES-256-GCM",
        integrity="GCM (Implicit)",
        mode="Transport"
    ),
    scenario_id="S03",
    filename="03-transport-gcm.pcap",
    packet_count=_s03_pkts,
    duration_sec=185.0,
    flow_count=len(S03_FLOWS),
    bytes_total=_s03_bytes,
    security_score=90,
    risk_level="LOW",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-GCM",
        integrity="GCM (Implicit)", dh_group="14 (modp2048)", pfs=True,
        authentication="PSK", mode="Transport", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S03_FLOWS,
    traffic_timeline=TIMELINE_S03,
    findings=[],
    report_metadata=_REPORT_META
)

# S04: AES-256-CBC / DH-4096
SCENARIO_RESULTS["S04"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S04",
        filename="04-cbc256-dh4096.pcap",
        display_name="Strong key exchange with legacy cipher mode",
        file_size_bytes=_s04_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(115.8),
        packet_count=_s04_pkts,
        ip_packet_count=int(_s04_pkts * 0.998),
        ipsec_packet_count=int(_s04_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="LOW",
        ike_version="IKEv2",
        encryption="AES-256-CBC",
        integrity="SHA-256",
        mode="Tunnel"
    ),
    scenario_id="S04",
    filename="04-cbc256-dh4096.pcap",
    packet_count=_s04_pkts,
    duration_sec=115.8,
    flow_count=len(S04_FLOWS),
    bytes_total=_s04_bytes,
    security_score=90,
    risk_level="LOW",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-CBC",
        integrity="SHA-256", dh_group="16 (modp4096)", pfs=True,
        authentication="PSK", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S04_FLOWS,
    traffic_timeline=TIMELINE_S04,
    findings=[
        SecurityFinding(
            id="FIND-010", severity="LOW", category="Encryption",
            title="CBC Mode Cipher (Non-AEAD)",
            description="AES-256-CBC requires a separate integrity algorithm (SHA-256). AEAD ciphers like AES-GCM provide authenticated encryption in a single construction, reducing attack surface and improving performance.",
            recommendation="Migrate to AES-256-GCM for authenticated encryption. Preserve the strong DH group.",
            status="OPEN",
            evidence=["IKE SA payload: AES-CBC-256 detected", "IPsec SA payload: HMAC-SHA-256 detected"],
            assessment="While AES-256-CBC with SHA-256 provides adequate security, CBC mode is vulnerable to padding oracle attacks if implementation flaws exist. Modern AEAD ciphers eliminate this class of vulnerability entirely. The strong 4096-bit DH group should be preserved or migrated to equivalent ECP.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = aes256-sha256-modp4096
+       proposals = aes256gcm16-prfsha384-modp4096
        children {
            net {
-               esp_proposals = aes256-sha256-modp4096
+               esp_proposals = aes256gcm16-modp4096
            }
        }
    }
}""",
            remediation_rationale="Migrating from CBC to GCM eliminates the separate HMAC step and provides authenticated encryption. The existing modp4096 DH group is preserved because it already exceeds minimum requirements.",
            remediation_validation="After applying, verify negotiated SA with: swanctl --list-sas. Confirm ENCR field shows AES_GCM_16 with 256-bit key. Confirm DH group remains modp4096. Verify PFS is still active.",
            evidence_type="OBSERVED"
        )
    ],
    report_metadata=_REPORT_META
)

# S05: No PFS
SCENARIO_RESULTS["S05"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S05",
        filename="05-no-pfs.pcap",
        display_name="Forward secrecy configuration issue",
        file_size_bytes=_s05_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(120.5),
        packet_count=_s05_pkts,
        ip_packet_count=int(_s05_pkts * 0.998),
        ipsec_packet_count=int(_s05_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="MEDIUM",
        ike_version="IKEv2",
        encryption="AES-256-GCM",
        integrity="GCM (Implicit)",
        mode="Tunnel"
    ),
    scenario_id="S05",
    filename="05-no-pfs.pcap",
    packet_count=_s05_pkts,
    duration_sec=120.5,
    flow_count=len(S05_FLOWS),
    bytes_total=_s05_bytes,
    security_score=70,
    risk_level="MEDIUM",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-GCM",
        integrity="GCM (Implicit)", dh_group="14 (modp2048)", pfs=False,
        authentication="PSK", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S05_FLOWS,
    traffic_timeline=TIMELINE_S05,
    findings=[
        SecurityFinding(
            id="FIND-003", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS. If the IKE keys are compromised, all IPsec traffic can be decrypted.",
            recommendation="Enable PFS with a strong Diffie-Hellman group in the IPsec configuration.",
            status="OPEN",
            evidence=["CREATE_CHILD_SA exchange lacks KE payload", "No ephemeral DH keys negotiated for IPsec SA"],
            assessment="Without Perfect Forward Secrecy (PFS), the IPsec session keys are derived entirely from the parent IKE SA. If an attacker records the encrypted traffic and later compromises the IKE credentials or IKE SA keys, they can decrypt all historical traffic retroactively.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
        children {
            net {
-               esp_proposals = aes256gcm16
+               esp_proposals = aes256gcm16-ecp256
            }
        }
    }
}""",
            remediation_rationale="Adding an ECP DH group to the ESP proposal enables Perfect Forward Secrecy for the CHILD SA. Each rekeying event will generate fresh ephemeral keys, preventing retroactive decryption if the IKE SA is compromised.",
            remediation_validation="After applying, verify with: swanctl --list-sas. The CHILD SA should show a DH group (e.g., ECP_256). During rekey, confirm CREATE_CHILD_SA includes a KE payload.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-004", severity="MEDIUM", category="Key Exchange",
            title="Session Key Reuse Risk",
            description="Without PFS, compromising one session key exposes all sessions using the same IKE SA keying material.",
            recommendation="Configure create-child-sa with a DH group to ensure independent keying per CHILD SA.",
            status="OPEN",
            evidence=["CHILD SA key derivation relies solely on IKE keying material"],
            assessment="Disabling PFS fundamentally weakens the compartmentalization of IPsec tunnels. The cryptographic health of the entire tunnel depends on a single point of failure.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
        children {
            net {
-               esp_proposals = aes256gcm16
+               esp_proposals = aes256gcm16-ecp256
            }
        }
    }
}""",
            remediation_rationale="Independent keying per CHILD SA via PFS ensures that compromising one session does not retroactively expose other sessions. This is the same configuration change as FIND-003.",
            remediation_validation="Same validation as FIND-003. Verify CREATE_CHILD_SA exchanges include KE payloads after configuration change.",
            evidence_type="DERIVED"
        )
    ],
    report_metadata=_REPORT_META
)

# S06: IKEv1 / 3DES / MD5
SCENARIO_RESULTS["S06"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S06",
        filename="06-weak-ikev1.pcap",
        display_name="Legacy protocol configuration",
        file_size_bytes=_s06_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(125.0),
        packet_count=_s06_pkts,
        ip_packet_count=int(_s06_pkts * 0.998),
        ipsec_packet_count=int(_s06_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="HIGH",
        ike_version="IKEv1",
        encryption="3DES",
        integrity="MD5",
        mode="Tunnel"
    ),
    scenario_id="S06",
    filename="06-weak-ikev1.pcap",
    packet_count=_s06_pkts,
    duration_sec=125.0,
    flow_count=len(S06_FLOWS),
    bytes_total=_s06_bytes,
    security_score=42,
    risk_level="HIGH",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv1", encryption="3DES",
        integrity="MD5", dh_group="2 (modp1024)", pfs=False,
        authentication="PSK", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S06_FLOWS,
    traffic_timeline=TIMELINE_S06,
    findings=[
        SecurityFinding(
            id="FIND-005", severity="HIGH", category="Protocol",
            title="Deprecated Protocol (IKEv1)",
            description="IKEv1 is obsolete and vulnerable to various attacks (e.g., Bleichenbacher, DoS).",
            recommendation="Migrate to IKEv2.",
            status="OPEN",
            evidence=["ISAKMP Header Version: 1.0 (IKEv1)"],
            assessment="IKEv1 (RFC 2409) was officially deprecated by IETF in 2018 (RFC 8436). It lacks built-in DoS protection, has complex and rigid negotiation phases (Main Mode/Aggressive Mode), and is susceptible to offline dictionary attacks if Aggressive Mode is used.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       version = 1
+       version = 2
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="IKEv2 provides built-in DoS protection (cookie mechanism), simpler negotiation, and support for modern cryptographic proposals. This patch simultaneously upgrades the protocol version and all cryptographic primitives.",
            remediation_validation="After applying, verify with: swanctl --list-sas. Confirm IKE version is 2. Confirm proposals show AES_GCM_16 and ECP_384. Verify tunnel establishment and bidirectional ESP traffic.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-006", severity="CRITICAL", category="Encryption",
            title="Weak Encryption (3DES)",
            description="3DES is cryptographically weak with an effective key size of 112 bits and is vulnerable to SWEET32 birthday attacks.",
            recommendation="Upgrade to AES-128 or AES-256.",
            status="OPEN",
            evidence=["SA Proposal: ENCR_3DES"],
            assessment="3DES operates on 64-bit blocks, making it highly vulnerable to birthday attacks (SWEET32). By capturing approximately 32 GB of traffic, an attacker can reliably produce collisions and recover plaintext secrets (like HTTP session cookies).",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="3DES uses 64-bit blocks and is vulnerable to SWEET32 birthday attacks after ~32 GB of captured traffic. AES-256-GCM provides 128-bit blocks with authenticated encryption, eliminating both the block size weakness and the need for a separate integrity algorithm.",
            remediation_validation="After applying, verify with: swanctl --list-sas. Confirm ENCR field shows AES_GCM_16 with 256-bit key. Ensure no 3DES or DES references remain in the negotiated SA.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-007", severity="CRITICAL", category="Integrity",
            title="Broken Hash Function (MD5)",
            description="MD5 is cryptographically broken and vulnerable to collision attacks. HMAC-MD5 provides reduced security margins.",
            recommendation="Upgrade to SHA-256 or better.",
            status="OPEN",
            evidence=["SA Proposal: AUTH_HMAC_MD5_96"],
            assessment="MD5 is completely broken. While HMAC construction protects against some known collision attacks, the security margin is extremely low and use of MD5 is prohibited by all modern compliance and security standards.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="MD5 is cryptographically broken. Migrating to AES-256-GCM eliminates the need for a separate integrity algorithm entirely, as GCM provides authenticated encryption with a 128-bit authentication tag.",
            remediation_validation="After applying, verify with: swanctl --list-sas. Confirm no MD5 or HMAC-MD5 references appear in the negotiated SA. Verify PRF uses SHA-384.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-008", severity="HIGH", category="Key Exchange",
            title="Perfect Forward Secrecy (PFS) Disabled",
            description="The CHILD SA was negotiated without PFS, leaving all sessions vulnerable if the IKE SA key is compromised.",
            recommendation="Enable PFS with a strong Diffie-Hellman group.",
            status="OPEN",
            evidence=["Quick Mode exchange lacks KE payload"],
            assessment="Without Perfect Forward Secrecy (PFS), the IPsec session keys are derived entirely from the parent IKE SA. If an attacker records the encrypted traffic and later compromises the IKE credentials, they can decrypt all historical traffic.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="Adding an ECP DH group to the CHILD SA ESP proposal enables PFS. Combined with the IKE proposal upgrade (FIND-005/006/007), this ensures independent keying for each CHILD SA rekey.",
            remediation_validation="After applying, verify with: swanctl --list-sas. The CHILD SA should show a DH group (e.g., ECP_384). Confirm CREATE_CHILD_SA includes KE payload during rekey.",
            evidence_type="OBSERVED"
        ),
        SecurityFinding(
            id="FIND-009", severity="HIGH", category="Key Exchange",
            title="Weak DH Group (modp1024)",
            description="DH group 2 (1024-bit MODP) is considered insufficient. NIST deprecated 1024-bit groups.",
            recommendation="Use DH group 14 (2048-bit) or stronger.",
            status="OPEN",
            evidence=["SA Proposal: DH Group 2 (1024-bit MODP)"],
            assessment="1024-bit Diffie-Hellman groups are vulnerable to nation-state level adversaries via the Logjam attack and general discrete logarithm precomputations. Modern infrastructure requires minimum 2048-bit MODP or Elliptic Curve groups.",
            remediation_config="""\
# /etc/swanctl/conf.d/ipsec_tunnel.conf
connections {
    vpn {
-       proposals = 3des-md5-modp1024
+       proposals = aes256gcm16-prfsha384-ecp384
        children {
            net {
-               esp_proposals = 3des-md5
+               esp_proposals = aes256gcm16-ecp384
            }
        }
    }
}""",
            remediation_rationale="1024-bit MODP groups are vulnerable to the Logjam attack. Migrating to ECP-384 provides equivalent security to ~7680-bit RSA/MODP while being computationally efficient. This eliminates the weak DH group at both the IKE and CHILD SA level.",
            remediation_validation="After applying, verify with: swanctl --list-sas. Confirm DH group shows ECP_384 for both IKE SA and CHILD SA. No modp1024 references should remain.",
            evidence_type="OBSERVED"
        )
    ],
    report_metadata=_REPORT_META
)

# S07: IPv6 / Tunnel / CNSA 2.0
SCENARIO_RESULTS["S07"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S07",
        filename="07-ipv6-tunnel.pcap",
        display_name="IPv6 tunnel scenario",
        file_size_bytes=_s07_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(110.0),
        packet_count=_s07_pkts,
        ip_packet_count=int(_s07_pkts * 0.998),
        ipsec_packet_count=int(_s07_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv6",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="SECURE",
        ike_version="IKEv2",
        encryption="AES-256-GCM",
        integrity="GCM (Implicit)",
        mode="Tunnel"
    ),
    scenario_id="S07",
    filename="07-ipv6-tunnel.pcap",
    packet_count=_s07_pkts,
    duration_sec=110.0,
    flow_count=len(S07_FLOWS),
    bytes_total=_s07_bytes,
    security_score=100,
    risk_level="SECURE",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-GCM",
        integrity="GCM (Implicit)", dh_group="31 (ECP521)", pfs=True,
        authentication="PSK", mode="Tunnel", ipv6=True,
        traffic_selectors="2001:db8:1::/64 === 2001:db8:2::/64"
    ),
    traffic_flows=S07_FLOWS,
    traffic_timeline=TIMELINE_S07,
    findings=[],
    report_metadata=_REPORT_META
)

# S08: X.509 certificate authentication
SCENARIO_RESULTS["S08"] = ScenarioAnalysis(
    capture=CaptureMetadata(
        id="S08",
        filename="08-cert-auth.pcap",
        display_name="Certificate-based authentication",
        file_size_bytes=_s08_bytes + 4096,
        capture_started_at="2026-09-28T09:12:00Z",
        duration_seconds=float(120.0),
        packet_count=_s08_pkts,
        ip_packet_count=int(_s08_pkts * 0.998),
        ipsec_packet_count=int(_s08_pkts * 0.996),
        ipsec_coverage_percent=99.6,
        protocol="ESP",
        ip_version="IPv4",
        interfaces=["eth0", "tun0"],
        source_type="TAP",
        analysis_status="ANALYZED",
        analysis_timestamp="2026-09-28T12:05:00Z",
        risk_level="LOW",
        ike_version="IKEv2",
        encryption="AES-256-GCM",
        integrity="GCM (Implicit)",
        mode="Tunnel"
    ),
    scenario_id="S08",
    filename="08-cert-auth.pcap",
    packet_count=_s08_pkts,
    duration_sec=120.0,
    flow_count=len(S08_FLOWS),
    bytes_total=_s08_bytes,
    security_score=98,
    risk_level="LOW",
    ipsec=IPSecInfo(
        protocol="ESP", ike_version="IKEv2", encryption="AES-256-GCM",
        integrity="GCM (Implicit)", dh_group="14 (modp2048)", pfs=True,
        authentication="X.509 Certificate (RSA)", mode="Tunnel", ipv6=False,
        traffic_selectors="10.0.1.0/24 === 10.0.2.0/24"
    ),
    traffic_flows=S08_FLOWS,
    traffic_timeline=TIMELINE_S08,
    findings=[],
    report_metadata=_REPORT_META
)


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
