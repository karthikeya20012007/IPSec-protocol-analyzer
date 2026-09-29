import re

# 1. Overview
with open('frontend/src/pages/Overview.tsx', 'r') as f:
    content = f.read()

new_header = """            <div className="mb-8">
                <div className="text-[11px] uppercase tracking-widest text-[#666C75] font-medium mb-1">OVERVIEW</div>
                <h2 className="text-[26px] font-semibold text-[#E7E9EC] tracking-wide mb-1">Security Analysis Overview</h2>
                <p className="text-[13px] text-[#969CA5]">High-level risk posture and capture metrics</p>
            </div>"""
content = re.sub(r'<h2 className="text-2xl font-medium text-white tracking-wide mb-6">Security Analysis Overview</h2>', new_header, content)

# update Top row metrics to match new Metric style inside cards if needed
# Actually I'll use regex to update Top row cards
content = re.sub(r'<span className="text-\[10px\] uppercase tracking-widest text-soc-text">([^<]+)</span>', r'<span className="text-[11px] uppercase tracking-wider text-[#969CA5] font-medium">\1</span>', content)
content = re.sub(r'<div className="p-4 font-mono text-sm text-white(?: truncate)?".*?>([^<]+)</div>', r'<div className="p-4 font-mono text-[26px] font-medium text-[#E7E9EC] truncate">\1</div>', content)
content = re.sub(r'<div className="p-4 font-mono text-xs text-white truncate" title=\{s\.capture\.filename\}>\{s\.capture\.filename\}</div>', r'<div className="p-4 font-mono text-[14px] font-medium text-[#E7E9EC] truncate" title={s.capture.filename}>{s.capture.filename}</div>', content)

# Update Security Findings sizes
content = re.sub(r'<h4 className="text-sm font-medium text-white mb-2">', r'<h4 className="text-[15px] font-semibold text-[#E7E9EC] mb-2">', content)
content = re.sub(r'<div className="text-xs text-soc-text-hover mb-3">', r'<div className="text-[13px] text-[#969CA5] mb-3">', content)

with open('frontend/src/pages/Overview.tsx', 'w') as f:
    f.write(content)

# 2. Captures
with open('frontend/src/pages/Captures.tsx', 'r') as f:
    content = f.read()

new_header = """            <div className="mb-6 border-b border-[#25282C] pb-5">
                <div className="text-[11px] uppercase tracking-widest text-[#666C75] font-medium mb-1">CAPTURES</div>
                <h2 className="text-[26px] font-semibold text-[#E7E9EC] tracking-wide mb-1">Capture Library</h2>
                <p className="text-[13px] text-[#969CA5]">Manage and analyze IPsec packet captures</p>
            </div>"""
content = re.sub(r'<div className="mb-2 border-b border-\[#1e2025\] pb-4">\s*<h2 className="text-2xl font-medium text-\[#e7e9ec\] tracking-wide">Capture Library</h2>\s*<p className="text-xs text-\[#969ca5\] mt-1">Manage and analyze IPsec packet captures</p>\s*</div>', new_header, content)

# Update Table content in Captures to 13-14px
content = re.sub(r'<th className="py-2.5 px-4 text-\[10px\] uppercase tracking-widest text-\[#666c75\] font-medium whitespace-nowrap">', r'<th className="py-2.5 px-4 text-[11px] uppercase tracking-widest text-[#666c75] font-medium whitespace-nowrap">', content)
content = re.sub(r'<td className="py-3 px-4 font-mono text-\[#3b82f6\] text-xs">', r'<td className="py-3 px-4 font-mono text-[#3b82f6] text-[13px]">', content)
content = re.sub(r'<td className="py-3 px-4 font-mono text-xs text-\[#e7e9ec\]">', r'<td className="py-3 px-4 font-mono text-[13px] text-[#e7e9ec]">', content)

with open('frontend/src/pages/Captures.tsx', 'w') as f:
    f.write(content)

