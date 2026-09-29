import React from 'react';
import type { AnalysisStage } from '../../context/AppContext';

interface AnalysisPipelineProps {
    currentStage: AnalysisStage | null;
    filename?: string;
}

const STAGES: { id: AnalysisStage; label: string; message: string }[] = [
    { id: 'CAPTURE_RECEIVED', label: 'CAPTURE RECEIVED', message: 'Receiving capture...' },
    { id: 'CAPTURE_VERIFIED', label: 'CAPTURE VERIFIED', message: 'Verifying capture integrity...' },
    { id: 'IPSEC_ANALYSIS', label: 'IPSEC ANALYSIS', message: 'Analyzing IKE / ESP configuration...' },
    { id: 'TRAFFIC_ANALYSIS', label: 'TRAFFIC ANALYSIS', message: 'Analyzing encrypted traffic behavior...' },
    { id: 'SECURITY_ASSESSMENT', label: 'SECURITY ASSESSMENT', message: 'Evaluating security posture...' },
    { id: 'REPORT_GENERATED', label: 'REPORT GENERATED', message: 'Preparing analysis report...' }
];

export const AnalysisPipeline: React.FC<AnalysisPipelineProps> = ({ currentStage, filename }) => {
    // Find index of current stage. If null, none are active.
    const currentIndex = currentStage ? STAGES.findIndex(s => s.id === currentStage) : -1;

    return (
        <div className="bg-[#0D0F10] border border-[#202326] rounded-sm p-6 max-w-md mx-auto w-full">
            <div className="mb-6 pb-4 border-b border-[#202326]">
                <h3 className="text-sm font-semibold text-[#E5E7EB] uppercase tracking-widest mb-1">Analysis Pipeline</h3>
                {filename ? (
                    <p className="text-xs font-mono text-[#8B9299] truncate" title={filename}>{filename}</p>
                ) : (
                    <p className="text-xs text-[#636C73]">Processing capture...</p>
                )}
            </div>

            <div className="space-y-4" role="status" aria-live="polite">
                {STAGES.map((stage, index) => {
                    const isCompleted = index < currentIndex;
                    const isActive = index === currentIndex;
                    const isPending = index > currentIndex;

                    return (
                        <div key={stage.id} className="flex flex-col">
                            <div className="flex items-center">
                                <div className={`
                                    flex items-center justify-center w-5 h-5 rounded-sm border text-[10px] mr-3
                                    ${isCompleted ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : ''}
                                    ${isActive ? 'bg-transparent border-[#E5E7EB] text-[#E5E7EB]' : ''}
                                    ${isPending ? 'bg-[#080909] border-[#202326] text-transparent' : ''}
                                `}>
                                    {isCompleted && '✓'}
                                    {isActive && (
                                        <svg 
                                            className="w-3 h-3 text-[#E5E7EB] animate-spin motion-reduce:animate-none" 
                                            xmlns="http://www.w3.org/2000/svg" 
                                            fill="none" 
                                            viewBox="0 0 24 24"
                                            aria-hidden="true"
                                        >
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                    )}
                                </div>
                                <span className={`text-xs uppercase tracking-widest ${
                                    isCompleted ? 'text-[#8B9299]' :
                                    isActive ? 'text-[#E5E7EB] font-medium' :
                                    'text-[#636C73]'
                                }`}>
                                    {stage.label}
                                </span>
                            </div>
                            
                            {/* Active stage description message */}
                            {isActive && (
                                <div className="ml-8 mt-1 text-xs text-[#8B9299] italic">
                                    {stage.message}
                                    <span className="sr-only"> - In progress</span>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
