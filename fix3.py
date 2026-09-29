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

import re
# First, remove old generated TIMELINE_ blocks
content = re.sub(r'TIMELINE_S0[1-8] = \[.*?\]\n', '', content, flags=re.DOTALL)

sizes = {}
for sid in ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"]:
    dur = float(re.search(rf'SCENARIO_RESULTS\["{sid}"\].*?duration_sec=([0-9.]+)', content, re.DOTALL).group(1))
    sizes[sid] = dur

imports_to_add = ""
for sid, dur in sizes.items():
    # We will inject the literal python variable names _s01_bytes, _s01_pkts etc.
    # Wait, we need the actual values to generate the python code.
    # We can just write code that executes and references those variables!
    # Ah, I can generate code that looks like:
    # _w_S01 = [...]
    # TIMELINE_S01 = [TrafficTimelinePoint(..., bytes=int(w * _s01_bytes)), ...]
    
    # Or just generate the weights in python code
    pass

import hashlib, math
def gen_weights(sid, duration):
    seed_str = f"{sid}_seed"
    val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    points = []
    num_points = 15
    interval = duration / num_points
    for i in range(num_points + 1):
        t = i * interval
        fluct = ((val + i * 997) % 100) / 100.0 
        base = 0.2 + 0.8 * (0.5 * (1 + math.sin(i * 0.5 + (val%10))))
        weight = base * (0.8 + 0.4 * fluct)
        points.append((int(t), weight))
    total_w = sum(w for t, w in points)
    return [(t, w/total_w) for t, w in points]

for sid, dur in sizes.items():
    weights = gen_weights(sid, dur)
    code = f"TIMELINE_{sid} = [\n"
    for t, w in weights:
        code += f"    TrafficTimelinePoint(timestamp={t}, packets=int({w} * _{sid.lower()}_pkts), bytes=int({w} * _{sid.lower()}_bytes)),\n"
    code += "]\n"
    imports_to_add += code

content = content.replace("SCENARIO_RESULTS = {}", imports_to_add + "\nSCENARIO_RESULTS = {}")

with open('backend/data/scenarios.py', 'w') as f:
    f.write(content)
