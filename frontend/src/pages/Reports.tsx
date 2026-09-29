import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { SeverityBadge } from '../components/common/SeverityBadge';

export const Reports: React.FC = () => {
    const { currentScenario } = useAppContext();
    const [reportType, setReportType] = useState<'EXECUTIVE' | 'TECHNICAL'>('EXECUTIVE');

    if (!currentScenario) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-[#636C73] text-sm">Select a capture to generate reports.</div>
            </div>
        );
    }

    const s = currentScenario;
    const findings = s.findings || [];
    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;
    const mediumCount = findings.filter(f => f.severity === 'MEDIUM').length;
    const lowCount = findings.filter(f => f.severity === 'LOW').length;

    // Derived Traffic Intelligence
    const classificationCounts: Record<string, number> = {};
    const totalFlows = s.traffic_flows?.length || 1;
    s.traffic_flows?.forEach(f => {
        classificationCounts[f.classification] = (classificationCounts[f.classification] || 0) + 1;
    });

    const triggerPrint = () => {
        window.print();
    };

    return (
        <div className="space-y-6">
            {/* Header / Action Bar (Hidden on Print) */}
            <div className="print:hidden mb-6 border-b border-[#202326] pb-5 flex justify-between items-end">
                <div>
                    <div className="text-xs uppercase tracking-widest text-[#636C73] font-medium mb-1">REPORTS</div>
                    <h2 className="text-2xl font-semibold text-[#E5E7EB] tracking-wide mb-1">Report Generation</h2>
                    <p className="text-sm text-[#8B9299]">Generate an executive or technical report for the selected capture.</p>
                </div>
                <div className="flex space-x-4">
                    <div className="flex bg-[#0D0F10] border border-[#202326] rounded-sm p-1">
                        <button
                            onClick={() => setReportType('EXECUTIVE')}
                            className={`px-4 py-1.5 text-sm uppercase tracking-widest font-medium rounded-sm transition-colors ${
                                reportType === 'EXECUTIVE' ? 'bg-[#202326] text-[#E5E7EB]' : 'text-[#636C73] hover:text-[#8B9299]'
                            }`}
                        >
                            Executive
                        </button>
                        <button
                            onClick={() => setReportType('TECHNICAL')}
                            className={`px-4 py-1.5 text-sm uppercase tracking-widest font-medium rounded-sm transition-colors ${
                                reportType === 'TECHNICAL' ? 'bg-[#202326] text-[#E5E7EB]' : 'text-[#636C73] hover:text-[#8B9299]'
                            }`}
                        >
                            Technical
                        </button>
                    </div>
                    <button
                        onClick={triggerPrint}
                        className="px-6 py-1.5 bg-[#3b82f6] hover:bg-[#60a5fa] text-white text-sm uppercase tracking-widest font-semibold rounded-sm transition-colors"
                    >
                        Download / Print
                    </button>
                </div>
            </div>

            {/* Report Document Surface */}
            <div className="bg-[#101213] border border-[#202326] p-10 md:p-16 max-w-5xl mx-auto shadow-2xl print:shadow-none print:border-none print:bg-white print:text-black print:p-0 print:m-0 print:w-full print:max-w-none">
                
                {/* Standard Document Header */}
                <div className="border-b-2 border-[#202326] print:border-black pb-8 mb-8 text-center md:text-left flex flex-col md:flex-row justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-bold text-[#E5E7EB] print:text-black tracking-tight mb-2">
                            {reportType === 'EXECUTIVE' ? 'Executive Security Summary' : 'Technical Analysis Report'}
                        </h1>
                        <p className="text-sm text-[#8B9299] print:text-[#555]">
                            IPsec Protocol Analyzer — Generated {s.report_metadata?.generated_at || new Date().toISOString().split('T')[0]}
                        </p>
                    </div>
                    <div className="mt-6 md:mt-0 text-right">
                        <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Target Capture</div>
                        <div className="font-mono text-[13px] text-[#E5E7EB] print:text-black font-semibold">{s.capture?.filename}</div>
                    </div>
                </div>

                {reportType === 'EXECUTIVE' && (
                    <div className="space-y-10">
                        {/* Summary Section */}
                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">IPsec Security Analysis</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 bg-[#0D0F10] print:bg-white border border-[#202326] print:border-gray-300 p-6">
                                <div>
                                    <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Risk Level</div>
                                    <div className="text-lg font-bold text-[#E5E7EB] print:text-black"><SeverityBadge severity={s.risk_level} /></div>
                                </div>
                                <div>
                                    <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Security Score</div>
                                    <div className="text-2xl font-mono font-semibold text-[#E5E7EB] print:text-black">{s.security_score}/100</div>
                                </div>
                                <div className="col-span-2">
                                    <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Findings Posture</div>
                                    <div className="flex space-x-4 text-[13px] font-mono">
                                        <span className="text-red-400 print:text-black">CRIT: {criticalCount}</span>
                                        <span className="text-orange-400 print:text-black">HIGH: {highCount}</span>
                                        <span className="text-amber-400 print:text-black">MED: {mediumCount}</span>
                                        <span className="text-emerald-400 print:text-black">LOW: {lowCount}</span>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">Executive Summary</h2>
                            <p className="text-sm text-[#E5E7EB] print:text-black leading-relaxed">
                                The capture <strong>{s.capture.filename}</strong> exhibits a <strong>{s.risk_level}</strong> risk profile with a security score of <strong>{s.security_score}/100</strong>. 
                                The IPsec tunnel was negotiated using {s.ipsec.ike_version} with {s.ipsec.encryption} encryption and {s.ipsec.integrity} integrity.
                                {criticalCount + highCount > 0 
                                    ? ` There are ${criticalCount + highCount} high-severity vulnerabilities identified in the cryptographic configuration that require immediate remediation to prevent traffic interception or key compromise.` 
                                    : ' The cryptographic posture is strong, aligning with modern security requirements.'}
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">IPsec Baseline</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4">
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">IKE Version</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.ike_version}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Encryption</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.encryption}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Integrity</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.integrity}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">PFS</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.pfs ? 'ENABLED' : 'DISABLED'}</div></div>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">Key Findings</h2>
                            {findings.length > 0 ? (
                                <div className="space-y-4">
                                    {findings.map(f => (
                                        <div key={f.id} className="border-l-2 border-[#3b82f6] print:border-gray-500 pl-4 py-1">
                                            <div className="flex items-center space-x-2 mb-1">
                                                <SeverityBadge severity={f.severity} />
                                                <span className="text-sm font-semibold text-[#E5E7EB] print:text-black">{f.title}</span>
                                            </div>
                                            <p className="text-sm text-[#8B9299] print:text-[#333] leading-relaxed">{f.assessment || f.description}</p>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-sm text-[#8B9299] print:text-[#555] italic">No significant security findings detected.</p>
                            )}
                        </section>

                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">Traffic Intelligence</h2>
                            <div className="flex flex-wrap gap-4">
                                {Object.entries(classificationCounts).map(([app, count]) => (
                                    <div key={app} className="bg-[#0D0F10] print:bg-gray-100 border border-[#202326] print:border-gray-300 px-4 py-2">
                                        <div className="text-sm font-medium text-[#E5E7EB] print:text-black">{app}</div>
                                        <div className="text-xs text-[#636C73] print:text-[#555] uppercase tracking-widest">{((count / totalFlows) * 100).toFixed(1)}% of Flows</div>
                                    </div>
                                ))}
                            </div>
                        </section>
                    </div>
                )}

                {reportType === 'TECHNICAL' && (
                    <div className="space-y-12">
                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">1. Capture Metadata</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 bg-[#0D0F10] print:bg-white border border-[#202326] print:border-gray-300 p-6">
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Filename</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.capture.filename}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Duration</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.capture.duration_seconds}s</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Packets</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.capture.packet_count.toLocaleString()}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">IPsec Coverage</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.capture.ipsec_coverage_percent.toFixed(1)}%</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">IP Version</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.ipv6 ? 'IPv6' : 'IPv4'}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">IPsec Protocol</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.protocol}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Risk Score</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.security_score}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Risk Level</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.risk_level}</div></div>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">2. IPsec Configuration</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 bg-[#0D0F10] print:bg-white border border-[#202326] print:border-gray-300 p-6">
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">IKE Version</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.ike_version}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Mode</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.mode.toUpperCase()}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Encryption</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.encryption}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Integrity</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.integrity}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">DH Group</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.dh_group}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">PFS</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.pfs ? 'ENABLED' : 'DISABLED'}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Authentication</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.authentication}</div></div>
                                <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-1">Selectors</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{s.ipsec.traffic_selectors}</div></div>
                            </div>
                        </section>

                        <section className="print:break-inside-avoid">
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">3. Security Assessment</h2>
                            {findings.length > 0 ? (
                                <div className="space-y-8">
                                    {findings.map(f => (
                                        <div key={f.id} className="border border-[#202326] print:border-gray-300 print:break-inside-avoid">
                                            <div className="bg-[#0D0F10] print:bg-gray-100 p-4 border-b border-[#202326] print:border-gray-300 flex items-center justify-between">
                                                <div className="flex items-center space-x-3">
                                                    <SeverityBadge severity={f.severity} />
                                                    <span className="text-base font-semibold text-[#E5E7EB] print:text-black">{f.title}</span>
                                                </div>
                                                <span className="text-xs font-mono text-[#636C73] print:text-[#555]">{f.id}</span>
                                            </div>
                                            <div className="p-6 space-y-6 bg-transparent print:bg-white">
                                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                                    <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555]">Category</div><div className="text-sm text-[#E5E7EB] print:text-black">{f.category}</div></div>
                                                    <div><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555]">Status</div><div className="text-sm text-[#E5E7EB] print:text-black font-mono">{f.status || 'OPEN'}</div></div>
                                                    <div className="col-span-2"><div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555]">Evidence Class</div><div className="text-sm text-[#3b82f6] print:text-[#2563eb] font-mono uppercase tracking-widest">{f.evidence_type || 'OBSERVED'}</div></div>
                                                </div>
                                                
                                                {f.evidence && f.evidence.length > 0 && (
                                                    <div>
                                                        <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-2 font-medium">Observed Evidence</div>
                                                        <ul className="list-disc pl-5 text-[13px] font-mono text-[#E5E7EB] print:text-black space-y-1">
                                                            {f.evidence.map((ev, i) => <li key={i}>{ev}</li>)}
                                                        </ul>
                                                    </div>
                                                )}

                                                <div>
                                                    <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-2 font-medium">Technical Assessment</div>
                                                    <p className="text-sm text-[#E5E7EB] print:text-black leading-relaxed">{f.assessment || f.description}</p>
                                                </div>

                                                <div>
                                                    <div className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-2 font-medium">Recommendation</div>
                                                    <p className="text-sm text-[#E5E7EB] print:text-black leading-relaxed">{f.recommendation}</p>
                                                </div>

                                                {f.remediation_config && (
                                                    <div className="mt-4 pt-4 border-t border-[#202326] print:border-gray-300">
                                                        <div className="text-xs uppercase tracking-widest text-[#3b82f6] print:text-[#2563eb] mb-2 font-medium">StrongSwan Remediation (Proposed)</div>
                                                        <div className="bg-[#080909] print:bg-white print:border print:border-gray-200 p-4 rounded-sm">
                                                            <pre className="font-mono text-xs leading-relaxed overflow-x-auto">
                                                                {f.remediation_config.split('\n').map((line, idx) => {
                                                                    let colorClass = "text-[#8B9299] print:text-gray-600";
                                                                    if (line.startsWith('+')) colorClass = "text-emerald-400 print:text-green-700";
                                                                    if (line.startsWith('-')) colorClass = "text-red-400 print:text-red-700";
                                                                    return <div key={idx} className={colorClass}>{line}</div>;
                                                                })}
                                                            </pre>
                                                        </div>
                                                        <div className="text-xs text-[#636C73] print:text-[#777] mt-2 italic">Configuration is a proposed remediation. Validated in staging environment before applying.</div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-sm text-[#8B9299] print:text-[#555]">No security findings present.</p>
                            )}
                        </section>
                        
                        <section className="print:break-inside-avoid">
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">4. Traffic Intelligence</h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h3 className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-3">Application Distribution</h3>
                                    <table className="w-full text-left border-collapse text-[13px]">
                                        <thead>
                                            <tr className="border-b border-[#202326] print:border-gray-300">
                                                <th className="py-2 text-xs uppercase tracking-widest text-[#8B9299] print:text-[#555] font-medium">Application</th>
                                                <th className="py-2 text-xs uppercase tracking-widest text-[#8B9299] print:text-[#555] font-medium text-right">Flow Count</th>
                                                <th className="py-2 text-xs uppercase tracking-widest text-[#8B9299] print:text-[#555] font-medium text-right">% of Traffic</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {Object.entries(classificationCounts).map(([app, count]) => (
                                                <tr key={app} className="border-b border-[#202326]/50 print:border-gray-200">
                                                    <td className="py-2 text-[#E5E7EB] print:text-black">{app}</td>
                                                    <td className="py-2 text-[#E5E7EB] print:text-black font-mono text-right">{count}</td>
                                                    <td className="py-2 text-[#E5E7EB] print:text-black font-mono text-right">{((count / totalFlows) * 100).toFixed(1)}%</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                                <div>
                                    <h3 className="text-xs uppercase tracking-widest text-[#636C73] print:text-[#555] mb-3">Classification Semantics</h3>
                                    <div className="space-y-4">
                                        <div className="p-4 bg-[#0D0F10] print:bg-white print:border print:border-gray-300">
                                            <div className="text-xs font-mono uppercase tracking-widest text-[#3b82f6] print:text-[#2563eb] mb-1">Derived</div>
                                            <p className="text-xs text-[#8B9299] print:text-[#444] leading-relaxed">
                                                AI/ML heuristic classification of encrypted flow behavior. Analyzes packet sizes, timing (IAT), throughput, and directionality without payload decryption.
                                            </p>
                                        </div>
                                        <div className="p-4 bg-[#0D0F10] print:bg-white print:border print:border-gray-300">
                                            <div className="text-xs font-mono uppercase tracking-widest text-emerald-400 print:text-green-600 mb-1">Observed</div>
                                            <p className="text-xs text-[#8B9299] print:text-[#444] leading-relaxed">
                                                Deterministic classification based on unencrypted handshakes, known port heuristics, or standard IANA parameters (e.g. ESP protocol 50).
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Protocol Composition Summary */}
                        <section className="print:break-inside-avoid">
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">5. Protocol Analysis</h2>
                            <div className="bg-[#0D0F10] print:bg-white print:border print:border-gray-300 p-6 flex flex-col space-y-2">
                                <div className="text-sm text-[#E5E7EB] print:text-black">
                                    The capture primarily consists of <strong>{s.ipsec.protocol}</strong> traffic utilizing <strong>{s.ipsec.mode.toUpperCase()}</strong> mode encapsulation.
                                </div>
                                <div className="text-sm text-[#E5E7EB] print:text-black">
                                    Negotiation was established over <strong>{s.ipsec.ike_version}</strong> via port 500/4500 UDP.
                                </div>
                            
                        <section className="print:break-inside-avoid mt-12 pt-8 border-t border-[#202326] print:border-gray-400">
                            <h2 className="text-sm font-bold uppercase tracking-widest text-[#E5E7EB] print:text-black border-b border-[#202326] print:border-gray-300 pb-2 mb-4">6. Assessment Methodology</h2>
                            <div className="space-y-4">
                                <p className="text-sm text-[#8B9299] print:text-[#333] leading-relaxed">
                                    The IPSec Protocol Analyzer evaluates captures passively. Cryptographic parameters are extracted via deep packet inspection of the unencrypted ISAKMP/IKE payloads. Security scoring is determined deterministically by comparing observed Phase 1 and Phase 2 proposals against modern compliance baselines (e.g., CNSA 2.0, NIST SP 800-52).
                                </p>
                                <p className="text-sm text-[#8B9299] print:text-[#333] leading-relaxed">
                                    Traffic intelligence utilizes statistical flow analysis on Encapsulating Security Payload (ESP) streams. Application classification confidence represents the model's heuristic certainty based on inter-arrival times (IAT), byte volume, and packet size distribution matching known traffic profiles. No payload decryption is performed during analysis.
                                </p>
                            </div>
                        </section>
</div>
                        </section>
                    </div>
                )}
            </div>
        </div>
    );
};
