import React from 'react';

interface StatusBadgeProps {
    value: string | boolean;
    trueLabel?: string;
    falseLabel?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ value, trueLabel = 'Enabled', falseLabel = 'Disabled' }) => {
    if (typeof value === 'boolean') {
        return (
            <span className={`inline-block text-xs font-medium uppercase tracking-widest px-2 py-0.5 rounded border ${
                value ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'
            }`}>
                {value ? trueLabel : falseLabel}
            </span>
        );
    }
    return (
        <span className="inline-block text-xs font-medium uppercase tracking-widest px-2 py-0.5 rounded border bg-white/5 text-soc-text-hover border-white/10">
            {value}
        </span>
    );
};
