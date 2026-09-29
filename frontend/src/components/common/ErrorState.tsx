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
    <div className="flex flex-col items-center justify-center py-16 text-center bg-[#0D0F10] border border-red-900/30 rounded-sm">
        <div className="w-12 h-12 rounded border border-red-500/20 bg-red-500/5 flex items-center justify-center mb-4">
            <span className="text-red-400 font-bold">!</span>
        </div>
        <h3 className="text-sm font-medium text-red-400 mb-2 uppercase tracking-widest">{title}</h3>
        <p className="text-sm text-[#8B9299] max-w-md mb-6">{message}</p>
        
        {onAction && (
            <button
                onClick={onAction}
                className="px-4 py-2 border border-[#202326] bg-[#080909] hover:bg-[#101213] text-[#E5E7EB] text-sm uppercase tracking-widest rounded-sm transition-colors"
            >
                {actionLabel}
            </button>
        )}
    </div>
);
