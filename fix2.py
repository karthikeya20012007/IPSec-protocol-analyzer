def _gen_timeline(scenario_id, total_bytes, total_pkts, duration):
    import hashlib, math
    seed_str = f"{scenario_id}_seed"
    val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    points = []
    num_points = 15
    interval = duration / num_points
    for i in range(num_points + 1):
        t = i * interval
        fluct = ((val + i * 997) % 100) / 100.0 
        base = 0.2 + 0.8 * (0.5 * (1 + math.sin(i * 0.5 + (val%10))))
        weight = base * (0.8 + 0.4 * fluct)
        points.append({'t': int(t), 'w': weight})
    total_w = sum(p['w'] for p in points)
    timeline = []
    for p in points:
        pts = int((p['w'] / total_w) * total_pkts)
        bts = int((p['w'] / total_w) * total_bytes)
        timeline.append(f"    TrafficTimelinePoint(timestamp={p['t']}, packets={pts}, bytes={bts})")
    return "[\n" + ",\n".join(timeline) + "\n]"

with open('backend/data/scenarios.py', 'r') as f:
    content = f.read()

# First we need to get the lengths of S01..S08 and their total_bytes/total_pkts.
import re
sizes = {}
for sid in ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"]:
    dur = float(re.search(rf'SCENARIO_RESULTS\["{sid}"\].*?duration_sec=([0-9.]+)', content, re.DOTALL).group(1))
    sizes[sid] = dur

imports_to_add = ""
for sid, dur in sizes.items():
    imports_to_add += f"TIMELINE_{sid} = " + _gen_timeline(sid, 1000000, 10000, dur) + "\n"

# Add TIMELINE_S0X to top
content = content.replace("SCENARIO_RESULTS = {}", imports_to_add + "\nSCENARIO_RESULTS = {}")

# Inject traffic_timeline=TIMELINE_S01, etc. into each ScenarioAnalysis
# Note: they might already have traffic_timeline from previous failed run if it wasn't removed properly
# Actually wait, I need to check if they already have it.
import re
for i in range(1, 9):
    sid = f"S0{i}"
    # Replace any existing traffic_timeline=TIMELINE_...,
    content = re.sub(rf"traffic_timeline=TIMELINE_{sid},\n\s*", "", content)
    # Then insert it
    content = content.replace(f"traffic_flows={sid}_FLOWS,", f"traffic_flows={sid}_FLOWS,\n    traffic_timeline=TIMELINE_{sid},")

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)
