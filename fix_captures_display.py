import re

with open('frontend/src/pages/Captures.tsx', 'r') as f:
    content = f.read()

# For the table, add "IKE" and "Risk" columns
new_th = """<th className="py-2.5 px-4 text-[10px] uppercase tracking-widest text-[#666c75] font-medium whitespace-nowrap">IPsec</th>
                                <th className="py-2.5 px-4 text-[10px] uppercase tracking-widest text-[#666c75] font-medium whitespace-nowrap">IKE</th>
                                <th className="py-2.5 px-4 text-[10px] uppercase tracking-widest text-[#666c75] font-medium whitespace-nowrap">Risk</th>
                                <th className="py-2.5 px-4 text-[10px] uppercase tracking-widest text-[#666c75] font-medium whitespace-nowrap">Action</th>"""
content = re.sub(r'<th className="py-2.5 px-4 text-\[10px\] uppercase tracking-widest text-\[#666c75\] font-medium whitespace-nowrap">IPsec</th>\s*<th className="py-2.5 px-4 text-\[10px\] uppercase tracking-widest text-\[#666c75\] font-medium whitespace-nowrap">Action</th>', new_th, content)

new_td = """<td className="py-3 px-4 font-mono text-xs text-[#e7e9ec]">{c.ipsec_coverage_percent}%</td>
                                    <td className="py-3 px-4 font-mono text-xs text-[#e7e9ec]">{c.ike_version}</td>
                                    <td className="py-3 px-4 font-mono text-xs text-[#e7e9ec]">{c.risk_level}</td>
                                    <td className="py-3 px-4">"""
content = re.sub(r'<td className="py-3 px-4 font-mono text-xs text-\[#e7e9ec\]">{c\.ipsec_coverage_percent}%</td>\s*<td className="py-3 px-4">', new_td, content)

# For the grid, add the metadata line
new_grid = """                                    <div className="text-[10px] text-[#666c75] font-mono mb-2 uppercase tracking-wide">
                                        {c.ike_version} · {c.protocol} · {c.encryption} · {c.mode}
                                    </div>
                                    <div className="flex flex-wrap gap-x-4 gap-y-2 mb-4">
                                        <div className="text-[10px] text-[#969ca5]"><span className="text-[#666c75] uppercase tracking-widest mr-1">Pkts</span><span className="font-mono">{c.packet_count.toLocaleString()}</span></div>
                                        <div className="text-[10px] text-[#969ca5]"><span className="text-[#666c75] uppercase tracking-widest mr-1">Dur</span><span className="font-mono">{c.duration_seconds}s</span></div>
                                        <div className="text-[10px] text-[#969ca5]"><span className="text-[#666c75] uppercase tracking-widest mr-1">IPsec</span><span className="font-mono">{c.ipsec_coverage_percent}%</span></div>
                                        <div className="text-[10px] text-[#969ca5]"><span className="text-[#666c75] uppercase tracking-widest mr-1">Risk</span><span className={`font-mono ${c.risk_level === 'CRITICAL' || c.risk_level === 'HIGH' ? 'text-red-400' : c.risk_level === 'MEDIUM' ? 'text-amber-400' : 'text-emerald-400'}`}>{c.risk_level}</span></div>
                                    </div>"""
content = re.sub(r'<div className="flex flex-wrap gap-x-4 gap-y-2 mb-4">\s*<div className="text-\[10px\] text-\[#969ca5\]"><span className="text-\[#666c75\] uppercase tracking-widest mr-1">Pkts</span><span className="font-mono">{c\.packet_count\.toLocaleString\(\)}</span></div>\s*<div className="text-\[10px\] text-\[#969ca5\]"><span className="text-\[#666c75\] uppercase tracking-widest mr-1">Dur</span><span className="font-mono">{c\.duration_seconds}s</span></div>\s*<div className="text-\[10px\] text-\[#969ca5\]"><span className="text-\[#666c75\] uppercase tracking-widest mr-1">IPsec</span><span className="font-mono">{c\.ipsec_coverage_percent}%</span></div>\s*</div>', new_grid, content)

with open('frontend/src/pages/Captures.tsx', 'w') as f:
    f.write(content)
