import re

with open('backend/data/scenarios.py', 'r') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith("def _gen_timeline("):
        skip = True
    if line.startswith('TIMELINE_S08 ='):
        skip = False
        continue
    if not skip:
        out.append(line)

with open('backend/data/scenarios.py', 'w') as f:
    f.writelines(out)

