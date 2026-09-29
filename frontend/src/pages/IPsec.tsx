import React from 'react';
import { useAppContext } from '../context/AppContext';
import { EmptyState } from '../components/common/EmptyState';
import { StatusBadge } from '../components/common/StatusBadge';
import { AnalyticalCard } from '../components/common/AnalyticalCard';
import { SectionHeader } from '../components/common/SectionHeader';
import { Metric } from '../components/common/MetricCard';
import { DonutChart } from '../components/charts/Charts';

export const IPsec: React.FC = () => {
    const { currentScenario } = useAppContext();

    if (!currentScenario) return <EmptyState />;

    const s = currentScenario;
    const ip = s.ipsec;

    // Protocol composition derived from scenario (mock logical distribution)
    const protocolComposition = [
        { name: 'ESP', bytes: s.bytes_total * 0.85, label: 'Encapsulating Security Payload' },
        { name: ip.ike_version, bytes: s.bytes_total * 0.10, label: 'Key Exchange' },
        { name: 'Other', bytes: s.bytes_total * 0.05, label: 'ARP, DNS, ICMP' },
    ];

    // Handshake timeline derived from IKE version
    const isV2 = ip.ike_version === 'IKEv2';
    const timeline = isV2
        ? [
            { step: 1, label: 'IKE_SA_INIT', desc: 'Propose crypto parameters, exchange nonces and DH values', status: 'complete', info: 'Phase 1 Init' },
            { step: 2, label: 'IKE_AUTH', desc: `Authenticate peers (${ip.authentication}), establish IKE SA`, status: 'complete', info: `Auth: ${ip.authentication}` },
            { step: 3, label: 'CREATE_CHILD_SA', desc: `Negotiate ESP SA: ${ip.encryption} / ${ip.integrity}`, status: 'complete', info: 'Phase 2 Child' },
            { step: 4, label: 'ESP ESTABLISHED', desc: `${ip.mode} mode tunnel active, traffic selectors: ${ip.traffic_selectors}`, status: 'active', info: 'Tunnel Active' },
        ]
        : [
            { step: 1, label: 'Main Mode (1-2)', desc: 'SA negotiation: propose crypto parameters', status: 'complete', info: 'Phase 1 Start' },
            { step: 2, label: 'Main Mode (3-4)', desc: `DH exchange: ${ip.dh_group}`, status: 'complete', info: `DH: ${ip.dh_group}` },
            { step: 3, label: 'Main Mode (5-6)', desc: `Authentication: ${ip.authentication}`, status: 'complete', info: `Auth: ${ip.authentication}` },
            { step: 4, label: 'Quick Mode', desc: `Negotiate ESP: ${ip.encryption} / ${ip.integrity}`, status: 'complete', info: 'Phase 2 ESP' },
            { step: 5, label: 'ESP ESTABLISHED', desc: `${ip.mode} mode tunnel active`, status: 'active', info: 'Tunnel Active' },
        ];

    const localNetwork = "10.0.1.0/24";
    const remoteNetwork = "10.0.2.0/24";

    return (
        <div className="space-y-6">
                        <div className="mb-6 border-b border-[#25282C] pb-5">
                <div className="text-xs uppercase tracking-widest text-[#666C75] font-medium mb-1">IPSEC</div>
                <h2 className="text-2xl font-semibold text-[#E7E9EC] tracking-wide mb-1">IPsec Protocol Analysis</h2>
                <p className="text-sm text-[#969CA5]">Cryptographic context and state</p>
            </div>

            {/* Context Bar */}
            <div className="flex flex-wrap items-center gap-4 bg-soc-panel border border-soc-border p-4 rounded-sm text-xs font-mono text-white shadow-sm">
                <span className="text-soc-accent font-medium px-2 py-1 bg-white/5 rounded border border-white/5">{ip.ike_version}</span>
                <span className="text-soc-border">/</span>
                <span className="px-2">{ip.mode.toUpperCase()} MODE</span>
                <span className="text-soc-border">/</span>
                <span className="px-2">ESP</span>
                <span className="text-soc-border">/</span>
                <span className="px-2">{ip.ipv6 ? 'IPv6' : 'IPv4'}</span>
                <span className="text-soc-border">/</span>
                <span className="px-2">{ip.encryption}</span>
                <span className="text-soc-border">/</span>
                <StatusBadge value={ip.pfs} trueLabel="PFS ENABLED" falseLabel="PFS DISABLED" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Cryptographic Parameters */}
                <AnalyticalCard>
                    <SectionHeader title="Cryptographic Parameters" subtitle="Phase 1 and Phase 2 configurations" />
                    <div className="grid grid-cols-2 gap-y-6 gap-x-4 mt-2">
                        <Metric label="Encryption" value={ip.encryption} />
                        <Metric label="Integrity" value={ip.integrity} />
                        <Metric label="DH Group" value={ip.dh_group} />
                        <Metric label="Authentication" value={ip.authentication} />
                    </div>
                </AnalyticalCard>

                {/* Traffic Selectors */}
                <AnalyticalCard>
                    <SectionHeader title="Traffic Selectors" subtitle={`Matched policies: ${ip.traffic_selectors}`} />
                    <div className="flex items-center justify-between mt-8 p-4 bg-soc-dark border border-soc-border rounded-sm relative overflow-hidden">
                        <div className="absolute inset-0 bg-soc-accent/5 pattern-grid-lg"></div>
                        <div className="relative flex flex-col items-center">
                            <div className="text-xs text-soc-text uppercase tracking-widest mb-2">Local Network</div>
                            <div className="font-mono text-white text-xs bg-white/5 px-3 py-1.5 rounded border border-white/10">{localNetwork}</div>
                        </div>
                        <div className="flex-1 mx-6 relative flex items-center justify-center">
                            <div className="absolute w-full h-px bg-soc-accent/50"></div>
                            <div className="absolute right-0 w-2 h-2 border-t border-r border-soc-accent/80 rotate-45 transform translate-x-[3px]"></div>
                            <div className="absolute left-0 w-2 h-2 border-t border-r border-soc-accent/80 rotate-[-135deg] transform -translate-x-[3px]"></div>
                            <div className="relative bg-soc-dark px-3 text-xs text-soc-accent uppercase tracking-widest font-mono border border-soc-accent/30 rounded-full py-1">IPsec ESP Tunnel</div>
                        </div>
                        <div className="relative flex flex-col items-center">
                            <div className="text-xs text-soc-text uppercase tracking-widest mb-2">Remote Network</div>
                            <div className="font-mono text-white text-xs bg-white/5 px-3 py-1.5 rounded border border-white/10">{remoteNetwork}</div>
                        </div>
                    </div>
                </AnalyticalCard>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* Security Association */}
                <AnalyticalCard className="col-span-1">
                    <SectionHeader title="Security Association" subtitle="Active tunnel parameters" />
                    <div className="grid grid-cols-1 gap-y-6 mt-2">
                        <Metric label="Protocol" value={ip.protocol} />
                        <Metric label="SPI Direction" value="Bidirectional" />
                        <Metric label="Replay Detection" value="Enabled" />
                        <Metric label="Anti-Replay Window" value="64 packets" />
                    </div>
                </AnalyticalCard>

                {/* Protocol Composition */}
                <AnalyticalCard className="col-span-1 flex flex-col">
                    <SectionHeader title="Protocol Composition" subtitle="Encapsulated traffic mix" />
                    <div className="flex-1 min-h-[240px] mt-2 relative">
                        <DonutChart data={protocolComposition} nameKey="name" dataKey="bytes" />
                    </div>
                </AnalyticalCard>

                {/* Handshake Timeline */}
                <AnalyticalCard className="col-span-1">
                    <SectionHeader title="IKE Handshake Sequence" subtitle={`${ip.ike_version} negotiation states`} />
                    <div className="relative mt-4 ml-2">
                        <div className="absolute left-[5px] top-2 bottom-2 w-px bg-white/10" />

                        <div className="space-y-6">
                            {timeline.map((t, i) => (
                                <div key={i} className="relative flex items-start pl-8">
                                    <div className={`absolute left-0 top-1.5 w-3 h-3 rounded-full border-[1.5px] ${
                                        t.status === 'active'
                                            ? 'bg-soc-accent border-soc-dark ring-2 ring-soc-accent/30'
                                            : 'bg-white/20 border-soc-panel'
                                    }`} />
                                    <div className="flex-1 bg-white/[0.02] border border-white/5 p-3 rounded-sm">
                                        <div className="flex items-center justify-between mb-1">
                                            <div className={`text-xs font-medium ${t.status === 'active' ? 'text-soc-accent' : 'text-white'}`}>{t.label}</div>
                                            <div className="text-xs text-soc-text/70 uppercase tracking-widest font-mono bg-white/5 px-2 py-0.5 rounded-sm">{t.info}</div>
                                        </div>
                                        <div className="text-sm text-soc-text">{t.desc}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </AnalyticalCard>
            </div>
        </div>
    );
};
