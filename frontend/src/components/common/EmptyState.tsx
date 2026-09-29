import React from 'react';

interface EmptyStateProps {
    title?: string;
    message?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
    title = 'No Capture Selected',
    message = 'Select a capture from the Captures page to begin analysis.'
}) => (
    <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center">
        <div className="w-16 h-16 rounded border-2 border-soc-border flex items-center justify-center mb-4">
            <div className="w-6 h-6 border-2 border-soc-text rounded-sm"></div>
        </div>
        <h3 className="text-lg font-medium text-soc-text-hover mb-1">{title}</h3>
        <p className="text-sm text-soc-text max-w-sm">{message}</p>
    </div>
);
