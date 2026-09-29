import React from 'react';
import type { AnalysisStage } from '../../context/AppContext';

interface AnalysisPipelineProps {
    currentStage: AnalysisStage | null;
    filename?: string;
}

const STAGES: { id: AnalysisStage; label: string }[] = [
    { id: 'CAPTURE_RECEIVED', label: 'CAPTURE RECEIVED' },
    { id: 'CAPTURE_VERIFIED', label: 'CAPTURE VERIFIED' },
    { id: 'IPSEC_ANALYSIS', label: 'IPSEC ANALYSIS' },
    { id: 'TRAFFIC_ANALYSIS', label: 'TRAFFIC ANALYSIS' },
    { id: 'SECURITY_ASSESSMENT', label: 'SECURITY ASSESSMENT' },
    { id: 'REPORT_GENERATED', label: 'REPORT GENERATED' }
];

export const AnalysisPipeline: React.FC<AnalysisPipelineProps> = ({ currentStage, filename }) => {
    // Find index of current stage. If null, none are active.
    const currentIndex = currentStage ? STAGES.findIndex(s => s.id === currentStage) : -1;

    return (
        <div className="bg-[#111315] border border-[#25282C] rounded-sm p-6 max-w-md mx-auto w-full">
            <div className="mb-6 pb-4 border-b border-[#25282C]">
                <h3 className="text-sm font-semibold text-[#E7E9EC] uppercase tracking-widest mb-1">Analysis Pipeline</h3>
                {filename ? (
                    <p className="text-xs font-mono text-[#969CA5] truncate" title={filename}>{filename}</p>
                ) : (
                    <p className="text-xs text-[#666C75]">Processing capture...</p>
                )}
            </div>

            <div className="space-y-4">
                {STAGES.map((stage, index) => {
                    const isCompleted = index < currentIndex;
                    const isActive = index === currentIndex;
                    const isPending = index > currentIndex;

                    return (
                        <div key={stage.id} className="flex items-center">
                            <div className={`
                                flex items-center justify-center w-5 h-5 rounded-sm border text-[10px] mr-3
                                ${isCompleted ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : ''}
                                ${isActive ? 'bg-[#0B0C0D] border-[#E7E9EC] text-[#E7E9EC]' : ''}
                                ${isPending ? 'bg-[#0B0C0D] border-[#25282C] text-transparent' : ''}
                            `}>
                                {isCompleted && '✓'}
                                {isActive && <div className="w-1.5 h-1.5 bg-[#E7E9EC] rounded-full animate-pulse" />}
                            </div>
                            <span className={`text-xs uppercase tracking-widest ${
                                isCompleted ? 'text-[#969CA5]' :
                                isActive ? 'text-[#E7E9EC] font-medium' :
                                'text-[#666C75]'
                            }`}>
                                {stage.label}
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
