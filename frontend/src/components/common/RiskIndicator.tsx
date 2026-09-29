import React from 'react';

interface RiskIndicatorProps {
    score: number;
    level: string;
    size?: 'sm' | 'lg' | 'xl';
}

const levelColor = (level: string) => {
    switch (level) {
        case 'CRITICAL': return { ring: 'text-[#ef4444]', bg: 'bg-[#ef4444]/10 border border-[#ef4444]/20', text: 'text-[#ef4444]' };
        case 'HIGH': return { ring: 'text-[#ef4444]', bg: 'bg-[#ef4444]/10 border border-[#ef4444]/20', text: 'text-[#ef4444]' };
        case 'MEDIUM': return { ring: 'text-[#f59e0b]', bg: 'bg-[#f59e0b]/10 border border-[#f59e0b]/20', text: 'text-[#f59e0b]' };
        case 'LOW': return { ring: 'text-[#22c55e]', bg: 'bg-[#22c55e]/10 border border-[#22c55e]/20', text: 'text-[#22c55e]' };
        case 'SECURE': return { ring: 'text-[#22c55e]', bg: 'bg-[#22c55e]/10 border border-[#22c55e]/20', text: 'text-[#22c55e]' };
        default: return { ring: 'text-[#636C73]', bg: 'bg-white/5 border border-white/10', text: 'text-[#636C73]' };
    }
};

export const RiskIndicator: React.FC<RiskIndicatorProps> = ({ score, level, size = 'lg' }) => {
    const colors = levelColor(level);
    const dim = size === 'xl' ? 180 : size === 'lg' ? 120 : 64;
    const r = size === 'xl' ? 76 : size === 'lg' ? 52 : 26;
    const stroke = size === 'xl' ? 6 : size === 'lg' ? 4 : 3;
    const circ = 2 * Math.PI * r;
    const offset = circ - (score / 100) * circ;

    return (
        <div className="flex flex-col items-center justify-center">
            <div className="relative flex items-center justify-center" style={{ width: dim, height: dim }}>
                <svg width={dim} height={dim} className="-rotate-90 absolute inset-0">
                    <circle cx={dim / 2} cy={dim / 2} r={r} fill="none" stroke="currentColor" strokeWidth={stroke} className="text-[#202326]" />
                    <circle cx={dim / 2} cy={dim / 2} r={r} fill="none" stroke="currentColor" strokeWidth={stroke} strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round" className={colors.ring} />
                </svg>
                <div className="flex flex-col items-center justify-center absolute inset-0">
                    <span className={`font-medium ${size === 'xl' ? 'text-6xl tracking-tight' : size === 'lg' ? 'text-4xl' : 'text-lg'} text-[#E5E7EB] leading-none`}>{score}</span>
                    {size !== 'sm' && <span className={`text-[10px] uppercase tracking-widest text-[#8B9299] ${size === 'xl' ? 'mt-2' : 'mt-1'}`}>/ 100</span>}
                </div>
            </div>
            <div className={`mt-6 px-3 py-1 rounded-sm text-[10px] font-semibold uppercase tracking-widest ${colors.bg} ${colors.text}`}>
                {level} RISK
            </div>
        </div>
    );
};
