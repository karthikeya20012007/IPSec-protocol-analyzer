import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { AnalyticalCard } from '../components/common/AnalyticalCard';
import { SectionHeader } from '../components/common/SectionHeader';
import { SeverityBadge } from '../components/common/SeverityBadge';
import { Metric } from '../components/common/MetricCard';
import { DetailDrawer } from '../components/common/DetailDrawer';
import type { SecurityFinding } from '../types';
import { EmptyState } from '../components/common/EmptyState';

export const Security: React.FC = () => {
    const { currentScenario } = useAppContext();
    const [selectedFinding, setSelectedFinding] = useState<SecurityFinding | null>(null);

    if (!currentScenario) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-[#636C73] text-sm">Select a capture to view security findings.</div>
            </div>
        );
    }

    const s = currentScenario;
    const findings = s.findings || [];

    if (findings.length === 0) {
        if (s.scenario_id === 'EX01') {
            return (
                <div className="pt-12">
                    <EmptyState 
                        title="Insufficient Evidence" 
                        message="Additional security conclusions cannot be derived from this capture because it does not contain enough observable protocol information."
                    />
                </div>
            );
        }
        return (
            <div className="pt-12">
                <EmptyState 
                    title="No Security Findings" 
                    message="No security findings were identified for this capture."
                />
            </div>
        );
    }


    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;
    const mediumCount = findings.filter(f => f.severity === 'MEDIUM').length;
    const lowCount = findings.filter(f => f.severity === 'LOW').length;

    const copyPatch = (e: React.MouseEvent, text: string) => {
        e.stopPropagation();
        navigator.clipboard.writeText(text);
    };

    const downloadPatch = (e: React.MouseEvent, text: string, filename: string) => {
        e.stopPropagation();
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <div className="space-y-6">
            <div className="mb-6 border-b border-[#202326] pb-5">
                <div className="text-xs uppercase tracking-widest text-[#636C73] font-medium mb-1">SECURITY</div>
                <h2 className="text-2xl font-semibold text-[#E5E7EB] tracking-wide mb-1">Security Assessment</h2>
                <p className="text-sm text-[#8B9299]">Protocol security findings, evidence, risk and remediation for the selected capture.</p>
            </div>

            {/* Posture Header */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
                <AnalyticalCard className="col-span-2 md:col-span-1 border-t-2 border-t-[#3b82f6]" noPadding>
                    <div className="p-4 border-b border-[#202326] bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#8B9299] font-medium">Risk Score</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-[#E5E7EB]">{s.security_score}/100</div>
                </AnalyticalCard>
                <AnalyticalCard className="col-span-2 md:col-span-1" noPadding>
                    <div className="p-4 border-b border-[#202326] bg-white/[0.02]">
                        <span className="text-xs uppercase tracking-wider text-[#8B9299] font-medium">Risk Level</span>
                    </div>
                    <div className="p-4 flex items-center h-[72px]">
                        <SeverityBadge severity={s.risk_level} />
                    </div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-[#202326] bg-red-500/5">
                        <span className="text-xs uppercase tracking-wider text-red-400 font-medium">Critical</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-red-400">{criticalCount}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-[#202326] bg-orange-500/5">
                        <span className="text-xs uppercase tracking-wider text-orange-400 font-medium">High</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-orange-400">{highCount}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-[#202326] bg-amber-500/5">
                        <span className="text-xs uppercase tracking-wider text-amber-400 font-medium">Medium</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-amber-400">{mediumCount}</div>
                </AnalyticalCard>
                <AnalyticalCard noPadding>
                    <div className="p-4 border-b border-[#202326] bg-emerald-500/5">
                        <span className="text-xs uppercase tracking-wider text-emerald-400 font-medium">Low</span>
                    </div>
                    <div className="p-4 font-mono text-2xl font-semibold text-emerald-400">{lowCount}</div>
                </AnalyticalCard>
            </div>

            {/* Observations */}
            <AnalyticalCard>
                <SectionHeader title="Observed IPsec Configuration" subtitle="Cryptographic baseline driving the security assessment" />
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-y-6 gap-x-4 mt-2">
                    <Metric label="IKE Version" value={s.ipsec.ike_version} accent />
                    <Metric label="Encryption" value={s.ipsec.encryption} />
                    <Metric label="Integrity" value={s.ipsec.integrity} />
                    <Metric label="DH Group" value={s.ipsec.dh_group} />
                    <Metric label="PFS" value={s.ipsec.pfs ? 'ENABLED' : 'DISABLED'} />
                    <Metric label="Authentication" value={s.ipsec.authentication} />
                    <Metric label="Mode" value={s.ipsec.mode.toUpperCase()} />
                    <Metric label="IP Version" value={s.ipsec.ipv6 ? 'IPv6' : 'IPv4'} />
                </div>
            </AnalyticalCard>

            {/* Findings Table */}
            <AnalyticalCard className="flex flex-col">
                <SectionHeader title="Security Findings" subtitle="Detected vulnerabilities and misconfigurations" />
                <div className="flex-1 mt-2">
                    {findings.length === 0 ? (
                        <div className="flex items-center justify-center h-48 border border-dashed border-[#202326] rounded-sm bg-[#0D0F10]">
                            <span className="text-emerald-500/80 text-sm">No security findings identified in this capture.</span>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="border-b border-[#202326] bg-white/[0.02]">
                                        <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Severity</th>
                                        <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Finding</th>
                                        <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Category</th>
                                        <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Status</th>
                                        <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {findings.map(f => (
                                        <tr 
                                            key={f.id} 
                                            className="border-b border-[#202326]/50 hover:bg-white/[0.02] cursor-pointer group transition-colors"
                                            onClick={() => setSelectedFinding(f)}
                                        >
                                            <td className="py-3 px-4 whitespace-nowrap"><SeverityBadge severity={f.severity} /></td>
                                            <td className="py-3 px-4 text-[#E5E7EB] text-sm font-medium">{f.title}</td>
                                            <td className="py-3 px-4 text-[#8B9299] text-sm whitespace-nowrap">{f.category}</td>
                                            <td className="py-3 px-4 font-mono text-[13px] text-[#8B9299] whitespace-nowrap">{f.status || 'OPEN'}</td>
                                            <td className="py-3 px-4 whitespace-nowrap text-right">
                                                <span className="text-xs text-[#3b82f6] opacity-0 group-hover:opacity-100 transition-opacity uppercase tracking-widest font-semibold">Review →</span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </AnalyticalCard>

            {/* Finding Detail Drawer */}
            <DetailDrawer
                open={!!selectedFinding}
                onClose={() => setSelectedFinding(null)}
                title="Finding Remediation"
            >
                {selectedFinding && (
                    <div className="space-y-6 pb-6">
                        {/* Title block */}
                        <div>
                            <div className="flex items-center space-x-3 mb-2">
                                <SeverityBadge severity={selectedFinding.severity} />
                                <span className="text-xs text-[#636C73] uppercase tracking-widest font-mono">{selectedFinding.id}</span>
                            </div>
                            <h4 className="text-lg font-semibold text-[#E5E7EB] leading-tight mb-2">{selectedFinding.title}</h4>
                            <div className="text-sm text-[#8B9299] leading-relaxed">{selectedFinding.description}</div>
                        </div>

                        {/* Workflow visual */}
                        <div className="flex items-center space-x-2 text-xs uppercase tracking-widest font-mono text-[#636C73]">
                            <span className="text-[#3b82f6]">Detected</span>
                            <span>→</span>
                            <span className={selectedFinding.assessment ? 'text-[#E5E7EB]' : ''}>Assessed</span>
                            <span>→</span>
                            <span className={selectedFinding.recommendation ? 'text-[#E5E7EB]' : ''}>Recommended</span>
                            <span>→</span>
                            <span className={selectedFinding.remediation_config ? 'text-[#E5E7EB]' : ''}>Patch Proposed</span>
                        </div>

                        {/* Evidence */}
                        <div className="bg-[#0D0F10] border border-[#202326] rounded-sm p-4 relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-1 h-full bg-[#3b82f6]/50"></div>
                            <div className="flex items-center justify-between mb-3">
                                <h5 className="text-sm uppercase tracking-widest text-[#8B9299] font-medium">Evidence</h5>
                                <span className="text-xs uppercase tracking-widest font-mono bg-[#3b82f6]/10 text-[#3b82f6] px-2 py-0.5 rounded-sm border border-[#3b82f6]/20">
                                    {selectedFinding.evidence_type || 'OBSERVED'}
                                </span>
                            </div>
                            <ul className="space-y-2 font-mono text-[13px] text-[#E5E7EB]">
                                {selectedFinding.evidence?.length > 0 ? (
                                    selectedFinding.evidence.map((ev, idx) => (
                                        <li key={idx} className="flex items-start">
                                            <span className="text-[#636C73] mr-2">›</span>
                                            <span>{ev}</span>
                                        </li>
                                    ))
                                ) : (
                                    <li className="text-[#8B9299] text-xs italic">Derived from protocol heuristics</li>
                                )}
                            </ul>
                        </div>

                        {/* Assessment */}
                        {selectedFinding.assessment && (
                            <div>
                                <h5 className="text-sm uppercase tracking-widest text-[#8B9299] font-medium mb-2 border-b border-[#202326] pb-2">Assessment</h5>
                                <p className="text-sm text-[#E5E7EB] leading-relaxed">{selectedFinding.assessment}</p>
                            </div>
                        )}

                        {/* Recommendation */}
                        <div>
                            <h5 className="text-sm uppercase tracking-widest text-[#8B9299] font-medium mb-2 border-b border-[#202326] pb-2">Recommendation</h5>
                            <p className="text-sm text-[#E5E7EB] leading-relaxed">{selectedFinding.recommendation}</p>
                        </div>

                        {/* Automated Remediation Patch */}
                        {selectedFinding.remediation_config ? (
                            <div>
                                <div className="flex items-center justify-between mb-2 border-b border-[#202326] pb-2">
                                    <div>
                                        <h5 className="text-sm uppercase tracking-widest text-[#8B9299] font-medium">Automated Remediation Patch</h5>
                                        <span className="text-xs text-[#636C73] font-mono">strongSwan / swanctl.conf</span>
                                    </div>
                                    <div className="flex space-x-2 items-center">
                                        <button 
                                            onClick={(e) => {
                                                copyPatch(e, selectedFinding.remediation_config);
                                                const btn = e.currentTarget;
                                                btn.textContent = 'Copied ✓';
                                                setTimeout(() => { btn.textContent = 'Copy Patch'; }, 2000);
                                            }}
                                            className="text-xs uppercase tracking-widest text-[#8B9299] hover:text-[#E5E7EB] transition-colors cursor-pointer bg-white/5 border border-[#202326] px-3 py-1.5 rounded-sm hover:bg-white/10"
                                        >
                                            Copy Patch
                                        </button>
                                        <button 
                                            onClick={(e) => downloadPatch(e, selectedFinding.remediation_config, `ipsec-remediation-${currentScenario.scenario_id}-${selectedFinding.id}.patch`)}
                                            className="text-xs uppercase tracking-widest text-[#8B9299] hover:text-[#E5E7EB] transition-colors cursor-pointer bg-white/5 border border-[#202326] px-3 py-1.5 rounded-sm hover:bg-white/10"
                                        >
                                            Download Patch
                                        </button>
                                    </div>
                                </div>
                                <div className="bg-[#080909] border border-[#202326] p-4 rounded-sm overflow-x-auto custom-scrollbar">
                                    <pre className="font-mono text-xs leading-relaxed">
                                        {selectedFinding.remediation_config.split('\n').map((line, idx) => {
                                            let colorClass = "text-[#8B9299]";
                                            let bgClass = "";
                                            if (line.startsWith('+')) {
                                                colorClass = "text-emerald-400";
                                                bgClass = "bg-emerald-500/10 block w-full";
                                            } else if (line.startsWith('-')) {
                                                colorClass = "text-red-400";
                                                bgClass = "bg-red-500/10 block w-full";
                                            } else if (line.startsWith('#')) {
                                                colorClass = "text-[#636C73] italic";
                                            }
                                            return (
                                                <span key={idx} className={`${colorClass} ${bgClass}`}>
                                                    {line}
                                                    {'\n'}
                                                </span>
                                            );
                                        })}
                                    </pre>
                                </div>

                                {/* Rationale */}
                                {selectedFinding.remediation_rationale && (
                                    <div className="mt-4">
                                        <h6 className="text-xs uppercase tracking-widest text-[#636C73] font-medium mb-1.5">Rationale</h6>
                                        <p className="text-sm text-[#8B9299] leading-relaxed">{selectedFinding.remediation_rationale}</p>
                                    </div>
                                )}

                                {/* Validation */}
                                {selectedFinding.remediation_validation && (
                                    <div className="mt-3">
                                        <h6 className="text-xs uppercase tracking-widest text-[#636C73] font-medium mb-1.5">Validation</h6>
                                        <p className="text-sm text-[#8B9299] leading-relaxed font-mono">{selectedFinding.remediation_validation}</p>
                                    </div>
                                )}

                                <p className="text-xs text-[#636C73] mt-3 italic border-t border-[#202326] pt-3">Generated remediation — review before applying. Do not apply patches without testing in a staging environment.</p>
                            </div>
                        ) : (
                            <div className="bg-[#0D0F10] border border-dashed border-[#202326] rounded-sm p-4 text-center">
                                <span className="text-sm text-[#636C73]">No remediation patch required.</span>
                            </div>
                        )}
                    </div>
                )}
            </DetailDrawer>
        </div>
    );
};
