import React, { useState, useMemo } from 'react';
import { useAppContext } from '../context/AppContext';
import { EmptyState } from '../components/common/EmptyState';
import { DetailDrawer } from '../components/common/DetailDrawer';
import { Metric } from '../components/common/MetricCard';
import { HorizontalBarChart, FlowBehaviorScatter, TrafficActivityAreaChart } from '../components/charts/Charts';
import type { TrafficFlow } from '../types';

export const Traffic: React.FC = () => {
    const { currentScenario } = useAppContext();
    const [selectedFlow, setSelectedFlow] = useState<TrafficFlow | null>(null);

    if (!currentScenario) return <EmptyState />;

    const s = currentScenario;

    const analytics = useMemo(() => {
        const classCounts: Record<string, { count: number; bytes: number; totalConf: number }> = {};
        let minConf = 1, maxConf = 0, totalConf = 0;
        let maxPkts = 0, totalDur = 0, totalThroughput = 0;

        s.traffic_flows.forEach(f => {
            if (!classCounts[f.classification]) classCounts[f.classification] = { count: 0, bytes: 0, totalConf: 0 };
            classCounts[f.classification].count += 1;
            classCounts[f.classification].bytes += f.bytes;
            classCounts[f.classification].totalConf += f.confidence;
            totalConf += f.confidence;
            if (f.confidence < minConf) minConf = f.confidence;
            if (f.confidence > maxConf) maxConf = f.confidence;
            if (f.packets > maxPkts) maxPkts = f.packets;
            totalDur += f.duration_sec;
            totalThroughput += f.throughput_bps;
        });

        const n = s.traffic_flows.length;
        const avgConf = n > 0 ? (totalConf / n * 100).toFixed(1) : '—';
        const avgDur = n > 0 ? (totalDur / n).toFixed(1) : '—';
        const avgPkts = n > 0 ? Math.round(s.traffic_flows.reduce((s, f) => s + f.packets, 0) / n) : 0;
        const avgThroughput = n > 0 ? (totalThroughput / n / 1000).toFixed(1) : '—';

        const distData = Object.entries(classCounts)
            .map(([name, v]) => ({
                name,
                count: v.count,
                bytes: v.bytes,
            }))
            .sort((a, b) => b.count - a.count);

        const confByApp = Object.entries(classCounts)
            .map(([name, v]) => ({
                name,
                confidence: Math.round((v.totalConf / v.count) * 100),
            }))
            .sort((a, b) => b.confidence - a.confidence);

        return {
            distData,
            confByApp,
            classCount: Object.keys(classCounts).length,
            avgConf,
            minConf: (minConf * 100).toFixed(0),
            maxConf: (maxConf * 100).toFixed(0),
            avgDur,
            avgPkts,
            avgThroughput,
            maxPkts,
        };
    }, [s]);

    const deriveFlowDetail = (f: TrafficFlow) => {
        const fwdPkts = Math.round(f.packets * 0.55);
        const bwdPkts = f.packets - fwdPkts;
        const bytesPerSec = f.duration_sec > 0 ? (f.bytes / f.duration_sec).toFixed(0) : '—';
        const pktsPerSec = f.duration_sec > 0 ? (f.packets / f.duration_sec).toFixed(1) : '—';
        const iatMean = f.duration_sec > 0 && f.packets > 1 ? ((f.duration_sec / (f.packets - 1)) * 1000).toFixed(2) : '—';
        return { fwdPkts, bwdPkts, bytesPerSec, pktsPerSec, iatMean };
    };

    return (
        <div className="space-y-4">
            {/* Page Header */}
                        <div className="mb-6 border-b border-[#25282C] pb-5">
                <div className="text-xs uppercase tracking-widest text-[#666C75] font-medium mb-1">TRAFFIC</div>
                <h2 className="text-2xl font-semibold text-[#E7E9EC] tracking-wide mb-1">Traffic Intelligence</h2>
                <p className="text-sm text-[#969CA5]">Encrypted traffic classification and flow behavior</p>
            </div>

            {/* Summary Strip */}
            <div className="grid grid-cols-4 gap-3">
                <div className="bg-[#111315] border border-[#25282C] rounded-sm px-4 py-3">
                    <div className="text-xs uppercase tracking-wider text-[#969CA5] font-medium mb-1.5">Total Flows</div>
                    <div className="text-2xl font-mono font-semibold text-[#E7E9EC]">{s.traffic_flows.length}</div>
                </div>
                <div className="bg-[#111315] border border-[#25282C] rounded-sm px-4 py-3">
                    <div className="text-xs uppercase tracking-wider text-[#969CA5] font-medium mb-1.5">Applications</div>
                    <div className="text-2xl font-mono font-semibold text-[#E7E9EC]">{analytics.classCount}</div>
                </div>
                <div className="bg-[#111315] border border-[#25282C] rounded-sm px-4 py-3">
                    <div className="text-xs uppercase tracking-wider text-[#969CA5] font-medium mb-1.5">Mean AI Confidence</div>
                    <div className="text-2xl font-mono font-semibold text-[#E7E9EC]">{analytics.avgConf}<span className="text-sm text-soc-text">%</span></div>
                </div>
                <div className="bg-[#111315] border border-[#25282C] rounded-sm px-4 py-3">
                    <div className="text-xs uppercase tracking-wider text-[#969CA5] font-medium mb-1.5">Encrypted Coverage</div>
                    <div className="text-2xl font-mono font-semibold text-[#E7E9EC]">100<span className="text-sm text-soc-text">%</span></div>
                </div>
            </div>

            {/* Analytics Row: Distribution + Scatter */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {/* Application Distribution */}
                <div className="bg-[#111315] border border-[#25282C] rounded-sm p-4">
                    <div className="flex items-baseline justify-between mb-3">
                        <div>
                            <h3 className="text-sm font-semibold text-[#E7E9EC] tracking-wide">Application Distribution</h3>
                            <p className="text-sm text-[#969CA5] mt-1">Flow count by inferred application</p>
                        </div>
                        <span className="text-xs text-soc-text uppercase tracking-widest">{analytics.distData.length} classes</span>
                    </div>
                    <div className="h-[280px]">
                        {analytics.distData.length > 0 ? (
                            <HorizontalBarChart data={analytics.distData} xKey="count" yKey="name" height={280} />
                        ) : (
                            <div className="h-full flex items-center justify-center text-sm text-soc-text">No flows</div>
                        )}
                    </div>
                </div>

                {/* Flow Behavior Scatter */}
                <div className="bg-[#111315] border border-[#25282C] rounded-sm p-4">
                    <div className="flex items-baseline justify-between mb-3">
                        <div>
                            <h3 className="text-sm font-semibold text-[#E7E9EC] tracking-wide">Flow Behavior</h3>
                            <p className="text-sm text-[#969CA5] mt-1">Flow duration vs packet volume</p>
                        </div>
                        <span className="text-xs text-soc-text uppercase tracking-widest">{s.traffic_flows.length} points</span>
                    </div>
                    <div className="h-[280px]">
                        {s.traffic_flows.length > 0 ? (
                            <FlowBehaviorScatter data={s.traffic_flows} height={280} />
                        ) : (
                            <div className="h-full flex items-center justify-center text-sm text-soc-text">No flows</div>
                        )}
                    </div>
                    <p className="text-sm text-soc-text mt-2 text-center">Each point represents one observed encrypted flow. Size proportional to byte volume.</p>
                </div>
            </div>

            {/* Traffic Activity (Timeline) */}
            <div className="bg-[#111315] border border-[#25282C] rounded-sm p-4">
                <div className="flex items-baseline justify-between mb-3">
                    <div>
                        <h3 className="text-sm font-semibold text-[#E7E9EC] tracking-wide">Traffic Activity</h3>
                        <p className="text-sm text-[#969CA5] mt-1">Encrypted traffic volume over capture timeline</p>
                    </div>
                    <span className="text-xs text-soc-text uppercase tracking-widest">{s.traffic_timeline?.length || 0} points</span>
                </div>
                <div className="h-[260px] w-full">
                    {s.traffic_timeline && s.traffic_timeline.length > 0 ? (
                        <TrafficActivityAreaChart data={s.traffic_timeline} height={260} />
                    ) : (
                        <div className="h-full flex items-center justify-center text-sm text-soc-text">No timeline data</div>
                    )}
                </div>
            </div>

            {/* Intelligence Row: Confidence + Characteristics */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
                {/* Classification Confidence */}
                <div className="lg:col-span-3 bg-[#111315] border border-[#25282C] rounded-sm p-4">
                    <h3 className="text-xs font-medium text-white uppercase tracking-widest mb-3">Classification Confidence</h3>
                    <div className="space-y-2.5">
                        {analytics.confByApp.map(c => (
                            <div key={c.name} className="flex items-center gap-3">
                                <span className="text-xs text-soc-text-hover w-28 shrink-0 truncate">{c.name}</span>
                                <div className="flex-1 h-2 bg-[#1a1c20] rounded-full overflow-hidden">
                                    <div
                                        className="h-full rounded-full transition-all"
                                        style={{
                                            width: `${c.confidence}%`,
                                            backgroundColor: c.confidence >= 90 ? '#10b981' : c.confidence >= 80 ? '#3b82f6' : c.confidence >= 70 ? '#f59e0b' : '#ef4444'
                                        }}
                                    />
                                </div>
                                <span className="text-xs font-mono text-white w-10 text-right">{c.confidence}%</span>
                            </div>
                        ))}
                    </div>
                    <div className="flex gap-6 mt-4 pt-3 border-t border-[#25282C] text-sm text-soc-text">
                        <span>Min: <span className="text-white font-mono">{analytics.minConf}%</span></span>
                        <span>Mean: <span className="text-white font-mono">{analytics.avgConf}%</span></span>
                        <span>Max: <span className="text-white font-mono">{analytics.maxConf}%</span></span>
                    </div>
                </div>

                {/* Traffic Characteristics */}
                <div className="lg:col-span-2 bg-[#111315] border border-[#25282C] rounded-sm p-4">
                    <h3 className="text-xs font-medium text-white uppercase tracking-widest mb-4">Traffic Characteristics</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Avg Flow Duration</span>
                            <span className="text-[13px] font-mono text-white">{analytics.avgDur}s</span>
                        </div>
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Avg Packets/Flow</span>
                            <span className="text-[13px] font-mono text-white">{analytics.avgPkts.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Avg Throughput</span>
                            <span className="text-[13px] font-mono text-white">{analytics.avgThroughput} Kbps</span>
                        </div>
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Largest Flow</span>
                            <span className="text-[13px] font-mono text-white">{analytics.maxPkts.toLocaleString()} pkts</span>
                        </div>
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Total Volume</span>
                            <span className="text-[13px] font-mono text-white">{(s.bytes_total / 1024 / 1024).toFixed(2)} MB</span>
                        </div>
                        <div className="flex justify-between items-baseline">
                            <span className="text-xs uppercase tracking-widest text-soc-text">Protocol</span>
                            <span className="text-[13px] font-mono text-soc-accent">{s.ipsec.protocol}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Flow Investigation Table */}
            <div className="bg-[#111315] border border-[#25282C] rounded-sm">
                <div className="px-4 py-3 border-b border-[#25282C] flex items-center justify-between">
                    <div>
                        <h3 className="text-sm font-semibold text-[#E7E9EC] tracking-wide">Observable Flows</h3>
                        <p className="text-sm text-[#969CA5] mt-1">{s.traffic_flows.length} flows · Click to inspect</p>
                    </div>
                    <div className="flex space-x-2">
                        <button className="text-sm uppercase tracking-widest text-soc-text px-2 py-1 bg-white/5 border border-white/10 rounded-sm hover:bg-white/10 transition-colors">Export</button>
                        <button className="text-sm uppercase tracking-widest text-soc-text px-2 py-1 bg-white/5 border border-white/10 rounded-sm hover:bg-white/10 transition-colors">Filter</button>
                    </div>
                </div>
                <div className="overflow-x-auto custom-scrollbar">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-[#25282C] bg-[#0B0C0D]">
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Flow</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Protocol</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Application</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Confidence</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Duration</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Packets</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap">Throughput</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#666C75] font-medium whitespace-nowrap"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {s.traffic_flows.map(f => (
                                <tr
                                    key={f.id}
                                    className="border-b border-[#14161a] hover:bg-[#151719] cursor-pointer transition-colors group"
                                    onClick={() => setSelectedFlow(f)}
                                >
                                    <td className="py-3 px-4 font-mono text-[#3b82f6] text-sm transition-colors whitespace-nowrap">{f.id}</td>
                                    <td className="py-3 px-4 text-[#969CA5] text-sm whitespace-nowrap">{s.ipsec.protocol}</td>
                                    <td className="py-2 px-4 whitespace-nowrap">
                                        <div className="flex items-center space-x-2">
                                            <span className="text-[#E7E9EC] text-sm">{f.classification}</span>
                                            <span className={`text-xs uppercase tracking-widest px-1.5 py-0.5 rounded-sm border ${
                                                f.is_inferred
                                                    ? 'bg-soc-accent/10 text-soc-accent border-soc-accent/20'
                                                    : 'bg-green-500/10 text-green-400 border-green-500/20'
                                            }`}>
                                                {f.is_inferred ? 'Derived' : 'Observed'}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="py-3 px-4 font-mono text-[13px] whitespace-nowrap">
                                        <span className={f.confidence >= 0.9 ? 'text-emerald-400' : f.confidence >= 0.8 ? 'text-soc-text-hover' : 'text-amber-400'}>
                                            {(f.confidence * 100).toFixed(0)}%
                                        </span>
                                    </td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E7E9EC] whitespace-nowrap">{f.duration_sec.toFixed(1)}s</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E7E9EC] whitespace-nowrap">{f.packets.toLocaleString()}</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E7E9EC] whitespace-nowrap">{(f.throughput_bps / 1000).toFixed(1)} Kbps</td>
                                    <td className="py-2 px-4 whitespace-nowrap">
                                        <span className="text-xs text-soc-accent opacity-0 group-hover:opacity-100 transition-opacity uppercase tracking-widest">Inspect →</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Flow Detail Drawer */}
            <DetailDrawer
                open={!!selectedFlow}
                onClose={() => setSelectedFlow(null)}
                title="Flow Investigation"
            >
                {selectedFlow && (() => {
                    const d = deriveFlowDetail(selectedFlow);
                    return (
                        <div className="space-y-6">
                            {/* Identity */}
                            <div className="bg-[#0B0C0D] border border-[#25282C] rounded-sm p-4">
                                <div className="text-xs text-soc-text uppercase tracking-widest mb-1">Flow ID</div>
                                <div className="font-mono text-white text-sm mb-3">{selectedFlow.id}</div>
                                <div className="flex items-center gap-3">
                                    <span className="text-lg font-medium text-white">{selectedFlow.classification}</span>
                                    <span className={`text-xs uppercase tracking-widest px-1.5 py-0.5 rounded-sm border ${
                                        selectedFlow.is_inferred
                                            ? 'bg-soc-accent/10 text-soc-accent border-soc-accent/20'
                                            : 'bg-green-500/10 text-green-400 border-green-500/20'
                                    }`}>
                                        {selectedFlow.is_inferred ? 'Derived (AI)' : 'Observed'}
                                    </span>
                                </div>
                            </div>

                            {/* Confidence */}
                            <div>
                                <div className="flex justify-between items-center text-xs mb-2">
                                    <span className="text-soc-text text-xs uppercase tracking-widest">Classification Confidence</span>
                                    <span className="font-mono text-white">{(selectedFlow.confidence * 100).toFixed(1)}%</span>
                                </div>
                                <div className="w-full h-1.5 bg-[#1a1c20] rounded-full overflow-hidden">
                                    <div className="h-full bg-soc-accent rounded-full" style={{ width: `${selectedFlow.confidence * 100}%` }} />
                                </div>
                                {selectedFlow.is_inferred && (
                                    <p className="text-sm text-soc-text leading-relaxed mt-2">
                                        Classification inferred from encrypted flow behavior. Does not imply payload decryption.
                                    </p>
                                )}
                            </div>

                            {/* Behavior Metrics */}
                            <div>
                                <h4 className="text-xs uppercase tracking-widest text-soc-text mb-3 pb-2 border-b border-[#25282C]">Behavior</h4>
                                <div className="grid grid-cols-2 gap-4">
                                    <Metric label="Duration" value={`${selectedFlow.duration_sec.toFixed(1)}s`} />
                                    <Metric label="Total Packets" value={selectedFlow.packets.toLocaleString()} />
                                    <Metric label="Fwd Packets" value={d.fwdPkts.toLocaleString()} />
                                    <Metric label="Bwd Packets" value={d.bwdPkts.toLocaleString()} />
                                    <Metric label="Throughput" value={`${(selectedFlow.throughput_bps / 1000).toFixed(1)} Kbps`} />
                                    <Metric label="Avg Pkt Size" value={`${selectedFlow.avg_packet_size} B`} />
                                    <Metric label="Bytes/sec" value={d.bytesPerSec} />
                                    <Metric label="Pkts/sec" value={d.pktsPerSec} />
                                    <Metric label="IAT Mean" value={`${d.iatMean} ms`} />
                                    <Metric label="Protocol" value={s.ipsec.protocol} />
                                </div>
                            </div>

                            {/* Signals */}
                            <div>
                                <h4 className="text-xs uppercase tracking-widest text-soc-text mb-3 pb-2 border-b border-[#25282C]">Observable Signals</h4>
                                <ul className="text-sm text-soc-text-hover space-y-2 font-mono">
                                    <li className="flex items-center space-x-2"><span className="text-soc-accent text-xs">▸</span><span>Packet size distribution</span></li>
                                    <li className="flex items-center space-x-2"><span className="text-soc-accent text-xs">▸</span><span>Inter-arrival time variance</span></li>
                                    <li className="flex items-center space-x-2"><span className="text-soc-accent text-xs">▸</span><span>Duration-to-volume ratio</span></li>
                                    <li className="flex items-center space-x-2"><span className="text-soc-accent text-xs">▸</span><span>Directional asymmetry</span></li>
                                </ul>
                            </div>
                        </div>
                    );
                })()}
            </DetailDrawer>
        </div>
    );
};
