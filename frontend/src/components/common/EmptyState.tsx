import React from 'react';

interface EmptyStateProps {
    title?: string;
    message?: string;
    action?: React.ReactNode;
    compact?: boolean;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
    title = 'No Capture Selected',
    message = 'Select a capture from the Captures page to begin analysis.',
    action,
    compact = false
}) => (
    <div className={`flex flex-col items-center justify-center text-center ${compact ? 'py-8' : 'h-full min-h-[400px]'}`}>
        {!compact && (
            <div className="w-12 h-12 rounded border-2 border-[#202326] flex items-center justify-center mb-4">
                <div className="w-4 h-4 border-2 border-[#636C73] rounded-sm"></div>
            </div>
        )}
        <h3 className="text-sm font-medium text-[#E5E7EB] mb-1 uppercase tracking-widest">{title}</h3>
        <p className="text-sm text-[#8B9299] max-w-sm">{message}</p>
        {action && <div className="mt-4">{action}</div>}
    </div>
);
