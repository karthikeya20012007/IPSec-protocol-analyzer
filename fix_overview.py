import re

with open('frontend/src/pages/Overview.tsx', 'r') as f:
    content = f.read()

# Replace the top metrics row in Overview
# Old row: Target Capture, Duration, Packets, Flows, Total Volume
# New row: Capture, Packets, Duration, IPsec Packets, IPsec Coverage, Flows, Total Volume
# I'll just rewrite the top row HTML block.

new_metrics = """
            {/* Top row: High-level metrics */}
            <div className="grid grid-cols-2 md:grid-cols-7 gap-4">
                <AnalyticalCard className="col-span-2 md:col-span-2" noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">Capture</span>
                    </div>
                    <div className="p-4 font-mono text-xs text-white truncate" title={s.capture.filename}>{s.capture.filename}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">Packets</span>
                    </div>
                    <div className="p-4 font-mono text-sm text-white">{s.capture.packet_count.toLocaleString()}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">Duration</span>
                    </div>
                    <div className="p-4 font-mono text-sm text-white">{s.capture.duration_seconds}s</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">IPsec Pkts</span>
                    </div>
                    <div className="p-4 font-mono text-sm text-white">{s.capture.ipsec_packet_count.toLocaleString()}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">Coverage</span>
                    </div>
                    <div className="p-4 font-mono text-sm text-white">{s.capture.ipsec_coverage_percent}%</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-[10px] uppercase tracking-widest text-soc-text">Flows</span>
                    </div>
                    <div className="p-4 font-mono text-sm text-white">{s.flow_count.toLocaleString()}</div>
                </AnalyticalCard>
            </div>
"""

old_metrics_regex = r"\{\/\* Top row: High-level metrics \*\/}.*?<\/div>"
content = re.sub(old_metrics_regex, new_metrics.strip(), content, flags=re.DOTALL)

# Also update the Executive Summary to use s.capture.filename
content = content.replace("s.filename", "s.capture.filename")

with open('frontend/src/pages/Overview.tsx', 'w') as f:
    f.write(content)
