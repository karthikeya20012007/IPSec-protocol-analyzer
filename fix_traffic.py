import re

with open('frontend/src/pages/Traffic.tsx', 'r') as f:
    content = f.read()

# Header
new_header = """            <div className="mb-6 border-b border-[#25282C] pb-5">
                <div className="text-[11px] uppercase tracking-widest text-[#666C75] font-medium mb-1">TRAFFIC</div>
                <h2 className="text-[26px] font-semibold text-[#E7E9EC] tracking-wide mb-1">Traffic Intelligence</h2>
                <p className="text-[13px] text-[#969CA5]">Encrypted traffic classification and flow behavior</p>
            </div>"""
content = re.sub(r'<div className="mb-2">\s*<h2 className="text-xl font-medium text-white tracking-wide">Traffic Intelligence</h2>\s*<p className="text-xs text-soc-text mt-1">Encrypted traffic classification and flow behavior analysis</p>\s*</div>', new_header, content)

# Summary Strip typography
content = re.sub(r'<div className="text-\[9px\] uppercase tracking-widest text-soc-text mb-1">', r'<div className="text-[11px] uppercase tracking-wider text-[#969CA5] font-medium mb-1.5">', content)
content = re.sub(r'<div className="text-2xl font-mono text-white">', r'<div className="text-[26px] font-mono font-medium text-[#E7E9EC]">', content)

# Headers in boxes
content = re.sub(r'<h3 className="text-xs font-medium text-white uppercase tracking-widest">', r'<h3 className="text-[15px] font-semibold text-[#E7E9EC] tracking-wide">', content)
content = re.sub(r'<p className="text-\[10px\] text-soc-text mt-0\.5">', r'<p className="text-[13px] text-[#969CA5] mt-1">', content)

# Table headers
content = re.sub(r'<th className="py-2 px-4 text-\[9px\] uppercase tracking-widest text-soc-text font-medium whitespace-nowrap">', r'<th className="py-2.5 px-4 text-[11px] uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">', content)

# Table body text
content = re.sub(r'<td className="py-2 px-4 font-mono text-soc-text-hover text-\[11px\] group-hover:text-white transition-colors whitespace-nowrap">', r'<td className="py-3 px-4 font-mono text-[#3b82f6] text-[13px] transition-colors whitespace-nowrap">', content)
content = re.sub(r'<td className="py-2 px-4 text-soc-text text-\[11px\] whitespace-nowrap">', r'<td className="py-3 px-4 text-[#969CA5] text-[13px] whitespace-nowrap">', content)
content = re.sub(r'<span className="text-white text-\[11px\]">', r'<span className="text-[#E7E9EC] text-[13px]">', content)
content = re.sub(r'<td className="py-2 px-4 font-mono text-\[11px\] whitespace-nowrap">', r'<td className="py-3 px-4 font-mono text-[13px] whitespace-nowrap">', content)
content = re.sub(r'<td className="py-2 px-4 font-mono text-\[11px\] text-soc-text whitespace-nowrap">', r'<td className="py-3 px-4 font-mono text-[13px] text-[#E7E9EC] whitespace-nowrap">', content)

# Color replacement
content = content.replace("bg-[#101214]", "bg-[#111315]")
content = content.replace("border-[#1e2025]", "border-[#25282C]")
content = content.replace("bg-[#0c0e10]", "bg-[#0B0C0D]")

with open('frontend/src/pages/Traffic.tsx', 'w') as f:
    f.write(content)
