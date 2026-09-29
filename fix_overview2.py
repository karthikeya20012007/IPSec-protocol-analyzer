import re

with open('frontend/src/pages/Overview.tsx', 'r') as f:
    content = f.read()

new_metrics = """            {/* Top row: High-level metrics */}
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

            {/* Risk Posture & Crypto Block */}"""

content = re.sub(r'\{\/\* Top row: High-level metrics \*\/\}.*?\{\/\* Risk Posture \& Crypto Block \*\/\}', new_metrics, content, flags=re.DOTALL)

with open('frontend/src/pages/Overview.tsx', 'w') as f:
    f.write(content)
