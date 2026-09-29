import React from 'react';

export const AnalyticalCard: React.FC<{ children: React.ReactNode; className?: string; noPadding?: boolean }> = ({ children, className = '', noPadding = false }) => (
    <div className={`bg-soc-panel border border-soc-border rounded-sm ${noPadding ? '' : 'p-6'} ${className}`}>
        {children}
    </div>
);
