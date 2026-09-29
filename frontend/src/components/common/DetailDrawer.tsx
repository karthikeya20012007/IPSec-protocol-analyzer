import React from 'react';

interface DetailDrawerProps {
    open: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
}

export const DetailDrawer: React.FC<DetailDrawerProps> = ({ open, onClose, title, children }) => {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex justify-end" onClick={onClose}>
            <div className="absolute inset-0 bg-black/50" />
            <div
                className="relative w-full max-w-md bg-soc-panel border-l border-soc-border h-full overflow-y-auto shadow-xl"
                onClick={e => e.stopPropagation()}
            >
                <div className="flex items-center justify-between px-6 py-4 border-b border-soc-border">
                    <h3 className="text-base font-semibold text-soc-text-hover tracking-wide">{title}</h3>
                    <button onClick={onClose} className="text-soc-text hover:text-soc-text-hover text-lg">&times;</button>
                </div>
                <div className="p-6">{children}</div>
            </div>
        </div>
    );
};
