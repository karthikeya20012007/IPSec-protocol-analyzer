import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, ScatterChart, Scatter, ZAxis, Legend, AreaChart, Area } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#64748b', '#ec4899', '#ef4444'];

// ── Tooltip ────────────────────────────────────
const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className="bg-[#0D0F10] border border-[#202326] px-3 py-2.5 rounded shadow-2xl text-xs">
                <div className="text-white font-medium mb-1.5">{label || payload[0]?.payload?.name || payload[0]?.name}</div>
                {payload.map((entry: any, index: number) => (
                    <div key={`item-${index}`} className="flex items-center space-x-2 text-xs">
                        <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: entry.color || entry.fill }} />
                        <span className="text-[#a1a1aa]">{entry.name || entry.dataKey}:</span>
                        <span className="text-white font-mono">{typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}</span>
                    </div>
                ))}
            </div>
        );
    }
    return null;
};

// Rich tooltip for scatter plot
const ScatterTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
        const d = payload[0]?.payload;
        if (!d) return null;
        return (
            <div className="bg-[#0D0F10] border border-[#202326] px-4 py-3 rounded shadow-2xl text-xs space-y-1.5">
                <div className="text-white font-medium text-sm mb-2">{d.classification}</div>
                <div className="flex justify-between gap-6"><span className="text-[#a1a1aa]">Flow ID</span><span className="text-white font-mono">{d.id}</span></div>
                <div className="flex justify-between gap-6"><span className="text-[#a1a1aa]">Duration</span><span className="text-white font-mono">{d.duration_sec}s</span></div>
                <div className="flex justify-between gap-6"><span className="text-[#a1a1aa]">Packets</span><span className="text-white font-mono">{d.packets.toLocaleString()}</span></div>
                <div className="flex justify-between gap-6"><span className="text-[#a1a1aa]">Throughput</span><span className="text-white font-mono">{(d.throughput_bps / 1000).toFixed(1)} Kbps</span></div>
                <div className="flex justify-between gap-6"><span className="text-[#a1a1aa]">Confidence</span><span className="text-white font-mono">{(d.confidence * 100).toFixed(0)}%</span></div>
            </div>
        );
    }
    return null;
};

// ── Donut Chart ────────────────────────────────
export const DonutChart: React.FC<{ data: any[], nameKey: string, dataKey: string }> = ({ data, nameKey, dataKey }) => (
    <ResponsiveContainer width="100%" height="100%">
        <PieChart>
            <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius="55%"
                outerRadius="80%"
                paddingAngle={2}
                dataKey={dataKey}
                nameKey={nameKey}
                stroke="none"
            >
                {data.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
        </PieChart>
    </ResponsiveContainer>
);

// ── Horizontal Bar Chart ───────────────────────
export const HorizontalBarChart: React.FC<{ data: any[], xKey: string, yKey: string, height?: number }> = ({ data, xKey, yKey, height }) => (
    <ResponsiveContainer width="100%" height={height || "100%"}>
        <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 4, right: 40, left: 4, bottom: 4 }}
        >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#1e2025" />
            <XAxis type="number" stroke="#71717a" fontSize={10} tickLine={false} axisLine={false} allowDecimals={false} />
            <YAxis dataKey={yKey} type="category" stroke="#a1a1aa" fontSize={11} tickLine={false} axisLine={false} width={110} />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: '#1e2025', opacity: 0.5 }} />
            <Bar dataKey={xKey} fill="#3b82f6" radius={[0, 3, 3, 0]} barSize={20} name="Flows">
                {data.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
            </Bar>
        </BarChart>
    </ResponsiveContainer>
);

// ── Scatter Plot ───────────────────────────────
export const FlowBehaviorScatter: React.FC<{ data: any[], height?: number }> = ({ data, height }) => {
    // Group data by classification for colored series
    const grouped: Record<string, any[]> = {};
    data.forEach(f => {
        if (!grouped[f.classification]) grouped[f.classification] = [];
        grouped[f.classification].push(f);
    });
    const series = Object.entries(grouped);

    return (
        <ResponsiveContainer width="100%" height={height || "100%"}>
            <ScatterChart margin={{ top: 10, right: 20, bottom: 30, left: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e2025" />
                <XAxis
                    type="number" dataKey="duration_sec" name="Duration"
                    stroke="#71717a" fontSize={10} tickLine={false}
                    label={{ value: 'Duration (s)', position: 'insideBottom', offset: -18, fill: '#71717a', fontSize: 10 }}
                />
                <YAxis
                    type="number" dataKey="packets" name="Packets"
                    stroke="#71717a" fontSize={10} tickLine={false}
                    label={{ value: 'Packets', angle: -90, position: 'insideLeft', offset: 10, fill: '#71717a', fontSize: 10 }}
                />
                <ZAxis type="number" dataKey="bytes" range={[60, 400]} name="Bytes" />
                <Tooltip content={<ScatterTooltip />} cursor={{ strokeDasharray: '3 3', stroke: '#3f3f46' }} />
                <Legend
                    verticalAlign="top" align="right" iconSize={8}
                    wrapperStyle={{ fontSize: 10, color: '#a1a1aa', paddingBottom: 8 }}
                />
                {series.map(([name, points], i) => (
                    <Scatter key={name} name={name} data={points} fill={COLORS[i % COLORS.length]} opacity={0.75} />
                ))}
            </ScatterChart>
        </ResponsiveContainer>
    );
};

// ── Traffic Activity Area Chart ────────────────
export const TrafficActivityAreaChart: React.FC<{ data: any[], height?: number }> = ({ data, height }) => (
    <ResponsiveContainer width="100%" height={height || "100%"}>
        <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 10, bottom: 20 }}
        >
            <defs>
                <linearGradient id="colorBytes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.05}/>
                </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e2025" vertical={false} />
            <XAxis
                dataKey="timestamp"
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                label={{ value: 'Timeline (s)', position: 'insideBottom', offset: -18, fill: '#71717a', fontSize: 10 }}
            />
                        <YAxis
                stroke="#71717a"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                domain={[0, 4096000]}
                ticks={[0, 1024000, 2048000, 3072000, 4096000]}
                tickFormatter={(value) => `${(value / 1024).toFixed(0)} KB`}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#3f3f46', strokeDasharray: '3 3' }} />
            <Area
                type="monotone"
                dataKey="bytes"
                name="Volume"
                stroke="#3b82f6"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorBytes)"
            />
        </AreaChart>
    </ResponsiveContainer>
);
