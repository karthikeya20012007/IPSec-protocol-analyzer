import React from 'react';

interface ErrorStateProps {
    title: string;
    message: string;
    onAction?: () => void;
    actionLabel?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
    title,
    message,
    onAction,
    actionLabel = 'Try Again'
}) => (
    <div className="flex flex-col items-center justify-center py-16 text-center bg-[#111315] border border-red-900/30 rounded-sm">
        <div className="w-12 h-12 rounded border border-red-500/20 bg-red-500/5 flex items-center justify-center mb-4">
            <span className="text-red-400 font-bold">!</span>
        </div>
        <h3 className="text-sm font-medium text-red-400 mb-2 uppercase tracking-widest">{title}</h3>
        <p className="text-sm text-[#969CA5] max-w-md mb-6">{message}</p>
        
        {onAction && (
            <button
                onClick={onAction}
                className="px-4 py-2 border border-[#25282C] bg-[#0B0C0D] hover:bg-[#17191C] text-[#E7E9EC] text-sm uppercase tracking-widest rounded-sm transition-colors"
            >
                {actionLabel}
            </button>
        )}
    </div>
);
