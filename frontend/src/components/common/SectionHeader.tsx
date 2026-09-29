import React from 'react';

export const SectionHeader: React.FC<{ title: string; subtitle?: string; action?: React.ReactNode }> = ({ title, subtitle, action }) => (
    <div className="flex items-end justify-between mb-5 pb-3 border-b border-[#202326]">
        <div>
            <h3 className="text-base font-semibold text-[#E5E7EB] tracking-wide">{title}</h3>
            {subtitle && <p className="text-sm text-[#8B9299] mt-1">{subtitle}</p>}
        </div>
        {action && <div>{action}</div>}
    </div>
);
