import React from 'react';

interface RiskIndicatorProps {
    score: number;
    level: string;
    size?: 'sm' | 'lg' | 'xl';
}

const levelColor = (level: string) => {
    switch (level) {
        case 'CRITICAL': return { ring: 'text-red-500/80', bg: 'bg-red-500/10 border border-red-500/20', text: 'text-red-400' };
        case 'HIGH': return { ring: 'text-orange-500/80', bg: 'bg-orange-500/10 border border-orange-500/20', text: 'text-orange-400' };
        case 'MEDIUM': return { ring: 'text-amber-500/80', bg: 'bg-amber-500/10 border border-amber-500/20', text: 'text-amber-400' };
        case 'LOW': return { ring: 'text-green-500/80', bg: 'bg-green-500/10 border border-green-500/20', text: 'text-green-400' };
        case 'SECURE': return { ring: 'text-emerald-500/80', bg: 'bg-emerald-500/10 border border-emerald-500/20', text: 'text-emerald-400' };
        default: return { ring: 'text-[#666C75]', bg: 'bg-white/5 border border-white/10', text: 'text-[#666C75]' };
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
        <div className="flex flex-col items-center">
            <svg width={dim} height={dim} className="-rotate-90">
                <circle cx={dim / 2} cy={dim / 2} r={r} fill="none" stroke="currentColor" strokeWidth={stroke} className="text-[#E7E9EC]/5" />
                <circle cx={dim / 2} cy={dim / 2} r={r} fill="none" stroke="currentColor" strokeWidth={stroke} strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round" className={colors.ring} />
            </svg>
            <div className="flex flex-col items-center -mt-[calc(50%+0.5rem)]" style={{ marginTop: size === 'xl' ? -112 : size === 'lg' ? -76 : -42 }}>
                <span className={`font-medium ${size === 'xl' ? 'text-6xl tracking-tight' : size === 'lg' ? 'text-4xl' : 'text-lg'} text-[#E7E9EC]`}>{score}</span>
                {size !== 'sm' && <span className={`text-xs uppercase tracking-widest text-[#666C75] ${size === 'xl' ? 'mt-1' : ''}`}>/ 100</span>}
            </div>
            <div className={`mt-${size === 'xl' ? '8' : size === 'lg' ? '6' : '2'} px-3 py-1 rounded text-xs font-medium uppercase tracking-widest ${colors.bg} ${colors.text}`}>
                {level} RISK
            </div>
        </div>
    );
};
