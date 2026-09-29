import React from 'react';

interface MetricProps {
    label: string;
    value: string | number;
    sub?: string;
    accent?: boolean;
}

export const Metric: React.FC<MetricProps> = ({ label, value, sub, accent }) => (
    <div className="flex flex-col">
        <div className="text-xs uppercase tracking-wider text-[#969CA5] mb-1.5 font-medium">{label}</div>
        <div className={`text-2xl font-mono font-semibold ${accent ? 'text-[#3b82f6]' : 'text-[#E7E9EC]'}`}>{value}</div>
        {sub && <div className="text-xs text-[#666C75] mt-1">{sub}</div>}
    </div>
);
