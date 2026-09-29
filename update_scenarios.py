import re

with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

timeline_defs = """
def _gen_timeline(scenario_id, total_bytes, total_pkts, duration):
    import hashlib
    # deterministic random based on scenario id
    seed_str = f"{scenario_id}_seed"
    val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    
    points = []
    num_points = 15
    interval = duration / num_points
    
    # generate a curve shape
    for i in range(num_points + 1):
        t = i * interval
        # pseudo random fluctuation
        fluct = ((val + i * 997) % 100) / 100.0 
        
        # Base curve: bell-ish shape or sine to make it look active
        base = 0.2 + 0.8 * (0.5 * (1 + __import__('math').sin(i * 0.5 + (val%10))))
        
        weight = base * (0.8 + 0.4 * fluct)
        points.append({'t': int(t), 'w': weight})
        
    total_w = sum(p['w'] for p in points)
    
    timeline = []
    for p in points:
        pts = int((p['w'] / total_w) * total_pkts)
        bts = int((p['w'] / total_w) * total_bytes)
        timeline.append(f'TrafficTimelinePoint(timestamp={p["t"]}, packets={pts}, bytes={bts})')
    
    return "[\n        " + ",\n        ".join(timeline) + "\n    ]"

TIMELINE_S01 = _gen_timeline("S01", _s01_bytes, _s01_pkts, 120.5)
TIMELINE_S02 = _gen_timeline("S02", _s02_bytes, _s02_pkts, 130.2)
TIMELINE_S03 = _gen_timeline("S03", _s03_bytes, _s03_pkts, 185.0)
TIMELINE_S04 = _gen_timeline("S04", _s04_bytes, _s04_pkts, 115.8)
TIMELINE_S05 = _gen_timeline("S05", _s05_bytes, _s05_pkts, 120.5)
TIMELINE_S06 = _gen_timeline("S06", _s06_bytes, _s06_pkts, 125.0)
TIMELINE_S07 = _gen_timeline("S07", _s07_bytes, _s07_pkts, 110.0)
TIMELINE_S08 = _gen_timeline("S08", _s08_bytes, _s08_pkts, 120.0)
"""

# Insert timeline definitions before SCENARIO_RESULTS = {}
content = content.replace("SCENARIO_RESULTS = {}", timeline_defs + "\nSCENARIO_RESULTS = {}")

# Inject traffic_timeline=TIMELINE_S01, etc. into each ScenarioAnalysis
for i in range(1, 9):
    sid = f"S0{i}"
    # find traffic_flows=S0X_FLOWS,
    search_str = f"traffic_flows={sid}_FLOWS,"
    replace_str = f"traffic_flows={sid}_FLOWS,\n    traffic_timeline=TIMELINE_{sid},"
    content = content.replace(search_str, replace_str)

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)
