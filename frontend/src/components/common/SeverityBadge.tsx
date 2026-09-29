import React from 'react';

interface SeverityBadgeProps {
    severity: string;
}

const severityStyles: Record<string, string> = {
    CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/20',
    HIGH: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    LOW: 'bg-green-500/10 text-green-400 border-green-500/20',
    INFO: 'bg-white/5 text-slate-300 border-white/10',
};

export const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity }) => (
    <span className={`inline-block text-xs font-medium uppercase tracking-widest px-2 py-0.5 rounded border ${severityStyles[severity] ?? severityStyles.INFO}`}>
        {severity}
    </span>
);
