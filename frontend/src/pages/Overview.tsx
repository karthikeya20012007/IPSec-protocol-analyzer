import React from 'react';
import { useAppContext } from '../context/AppContext';
import { EmptyState } from '../components/common/EmptyState';
import { Metric } from '../components/common/MetricCard';
import { RiskIndicator } from '../components/common/RiskIndicator';
import { SeverityBadge } from '../components/common/SeverityBadge';
import { SectionHeader } from '../components/common/SectionHeader';
import { AnalyticalCard } from '../components/common/AnalyticalCard';
import { DonutChart } from '../components/charts/Charts';

export const Overview: React.FC = () => {
    const { currentScenario } = useAppContext();

    if (!currentScenario) return <EmptyState />;

    const s = currentScenario;

    // Derive traffic distribution from flows
    const classCounts: Record<string, number> = {};
    s.traffic_flows.forEach(f => {
        classCounts[f.classification] = (classCounts[f.classification] || 0) + f.bytes;
    });
    const distributionData = Object.entries(classCounts).map(([name, bytes]) => ({
        name,
        bytes,
        label: `${(bytes / 1024).toFixed(0)} KB`
    })).sort((a, b) => b.bytes - a.bytes);

    const avgConfidence = s.traffic_flows.length > 0
        ? (s.traffic_flows.reduce((sum, f) => sum + f.confidence, 0) / s.traffic_flows.length * 100).toFixed(1)
        : '—';

    return (
        <div className="space-y-6">
                        <div className="mb-8">
                <div className="text-xs uppercase tracking-widest text-[#666C75] font-medium mb-1">OVERVIEW</div>
                <h2 className="text-2xl font-semibold text-[#E7E9EC] tracking-wide mb-1">Security Analysis Overview</h2>
                <p className="text-sm text-[#969CA5]">High-level risk posture and capture metrics</p>
            </div>

                        {/* Top row: High-level metrics */}
            <div className="grid grid-cols-2 md:grid-cols-7 gap-4">
                <AnalyticalCard className="col-span-2 md:col-span-2" noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">Capture</span>
                    </div>
                    <div className="p-4 font-mono text-[13px] font-medium text-[#E7E9EC] truncate" title={s.capture.filename}>{s.capture.filename}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">Packets</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E7E9EC] truncate">{s.capture.packet_count.toLocaleString()}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">Duration</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E7E9EC] truncate">{s.capture.duration_seconds}s</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">IPsec Pkts</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E7E9EC] truncate">{s.capture.ipsec_packet_count.toLocaleString()}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">Coverage</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E7E9EC] truncate">{s.capture.ipsec_coverage_percent}%</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-white/5 bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#969CA5] font-medium">Flows</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E7E9EC] truncate">{s.flow_count.toLocaleString()}</div>
                </AnalyticalCard>
            </div>

            {/* Risk Posture & Crypto Block */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <AnalyticalCard className="col-span-1 lg:col-span-5 flex flex-col relative overflow-hidden">
                    <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${s.risk_level === 'CRITICAL' || s.risk_level === 'HIGH' ? 'from-red-500/40' : s.risk_level === 'MEDIUM' ? 'from-amber-500/40' : 'from-green-500/40'} via-transparent to-transparent`}></div>
                    <SectionHeader title="Risk Posture" subtitle="Overall security assessment of capture" />
                    <div className="flex-1 flex flex-col items-center justify-center py-6">
                        <RiskIndicator score={s.security_score} level={s.risk_level} size="xl" />
                    </div>
                </AnalyticalCard>

                <AnalyticalCard className="col-span-1 lg:col-span-7">
                    <SectionHeader title="IPsec Security Context" subtitle="Observed cryptographic baseline" />
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-y-8 gap-x-6 mt-4">
                        <Metric label="IKE Version" value={s.ipsec.ike_version} accent />
                        <Metric label="Encryption" value={s.ipsec.encryption} />
                        <Metric label="Integrity" value={s.ipsec.integrity} />
                        <Metric label="PFS" value={s.ipsec.pfs ? 'ENABLED' : 'DISABLED'} />
                        <Metric label="Authentication" value={s.ipsec.authentication} />
                        <Metric label="Mode" value={s.ipsec.mode.toUpperCase()} />
                        <Metric label="DH Group" value={s.ipsec.dh_group} />
                        <Metric label="IP Version" value={s.ipsec.ipv6 ? 'IPv6' : 'IPv4'} />
                    </div>
                </AnalyticalCard>
            </div>

            {/* Lower row: Traffic & Findings */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <AnalyticalCard className="flex flex-col">
                    <SectionHeader 
                        title="Traffic Intelligence" 
                        subtitle="Inferred application distribution (by byte volume)"
                        action={<span className="text-xs uppercase tracking-widest text-soc-accent font-mono bg-soc-accent/10 px-2 py-1 rounded border border-soc-accent/20">AI Confidence: {avgConfidence}%</span>}
                    />
                    <div className="flex-1 min-h-[300px] mt-4 relative">
                        {distributionData.length > 0 ? (
                            <DonutChart data={distributionData} nameKey="name" dataKey="bytes" />
                        ) : (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-4">
                                <span className="text-sm font-medium text-[#E7E9EC] uppercase tracking-widest mb-1">Insufficient Evidence</span>
                                <span className="text-xs text-[#969CA5]">Additional traffic conclusions cannot be derived from this capture.</span>
                            </div>
                        )}
                    </div>
                </AnalyticalCard>

                <AnalyticalCard className="flex flex-col">
                    <SectionHeader title="Security Findings" subtitle="Detected vulnerabilities and misconfigurations" />
                    <div className="flex-1 overflow-y-auto custom-scrollbar pr-2 mt-4 space-y-4">
                        {s.findings.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-48 border border-dashed border-[#25282C] rounded-sm bg-[#111315]">
                                <span className="text-[#E7E9EC] text-sm font-medium uppercase tracking-widest mb-1">
                                    {s.scenario_id === 'EX01' ? 'Insufficient Evidence' : 'No Security Findings'}
                                </span>
                                <span className="text-xs text-[#969CA5] text-center px-4">
                                    {s.scenario_id === 'EX01' 
                                        ? 'Security conclusions cannot be derived from this capture.' 
                                        : 'No security findings identified.'}
                                </span>
                            </div>
                        ) : (
                            s.findings.map(f => (
                                <div key={f.id} className="bg-soc-dark border border-soc-border rounded-sm p-4">
                                    <div className="flex items-start justify-between mb-3">
                                        <div className="flex items-center space-x-3">
                                            <SeverityBadge severity={f.severity} />
                                            <span className="text-xs text-soc-text uppercase tracking-widest">{f.category}</span>
                                        </div>
                                    </div>
                                    <h4 className="text-base font-semibold text-[#E7E9EC] mb-2">{f.title}</h4>
                                    <div className="text-sm text-[#969CA5] mb-3">{f.description}</div>
                                    
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 pt-4 border-t border-white/5">
                                        <div>
                                            <div className="text-xs uppercase tracking-widest text-soc-text mb-1">Evidence</div>
                                            <div className="text-xs font-mono text-soc-accent">Derived from protocol heuristics</div>
                                        </div>
                                        <div>
                                            <div className="text-xs uppercase tracking-widest text-soc-text mb-1">Recommendation</div>
                                            <div className="text-xs text-soc-text-hover">{f.recommendation}</div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </AnalyticalCard>
            </div>

            {/* Executive Analysis */}
            <AnalyticalCard>
                <SectionHeader title="Executive Summary" />
                <p className="text-sm text-soc-text-hover leading-relaxed max-w-5xl mt-2">
                    Analysis of <span className="font-mono text-white px-1 bg-white/5 rounded mx-1">{s.capture.filename}</span> indicates a 
                    <span className={`font-medium px-1.5 py-0.5 rounded ml-1 mr-1 ${s.risk_level === 'CRITICAL' || s.risk_level === 'HIGH' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-white/5 text-white'}`}>
                        {s.risk_level}
                    </span> 
                    risk posture. The IPsec tunnel was established using {s.ipsec.ike_version} with {s.ipsec.encryption} encryption and {s.ipsec.integrity} integrity. 
                    {s.ipsec.pfs ? ' Perfect Forward Secrecy (PFS) is correctly configured, ensuring session key isolation.' : ' Perfect Forward Secrecy (PFS) is missing, compromising forward secrecy.'}
                    {s.findings.length > 0 && ` Immediate remediation is recommended for identified vulnerabilities.`}
                </p>
            </AnalyticalCard>
        </div>
    );
};
