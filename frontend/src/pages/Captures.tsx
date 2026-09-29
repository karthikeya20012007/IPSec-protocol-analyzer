import { useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from 'react';
import { useAppContext } from '../context/AppContext';
import type { AnalysisStage } from '../context/AppContext';
import { apiClient } from '../api/client';
import { SectionHeader } from '../components/common/SectionHeader';
import { AnalysisPipeline } from '../components/common/AnalysisPipeline';
import { ErrorState } from '../components/common/ErrorState';
import type { CaptureMetadata } from '../types';

export const Captures: React.FC = () => {
    const navigate = useNavigate();
    const { 
        setScenario, setLoading, setError, isLoading, error,
        uploadStatus, setUploadStatus, analysisStage, setAnalysisStage,
        uploadError, setUploadError, resetUploadState
    } = useAppContext();
    const [captures, setCaptures] = useState<CaptureMetadata[]>([]);
    const [selectedFilename, setSelectedFilename] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        apiClient.getScenarios()
            .then(setCaptures)
            .catch(() => setError("Failed to load demo scenarios"));
    }, [setError]);

    const handleSelect = async (scenarioId: string) => {
        setLoading(true);
        setError(null);
        try {
            const data = await apiClient.analyzeScenario(scenarioId);
            setScenario(data);
            navigate('/app/overview');
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        resetUploadState();
        setSelectedFilename(file.name);

        if (!file.name.endsWith('.pcap') && !file.name.endsWith('.pcapng')) {
            setUploadError({
                title: 'UNSUPPORTED FILE TYPE',
                message: 'Supported formats: PCAP, PCAPNG'
            });
            setUploadStatus('ERROR');
            return;
        }

        if (file.size === 0) {
            setUploadError({
                title: 'EMPTY CAPTURE',
                message: 'The selected file contains no capture data.'
            });
            setUploadStatus('ERROR');
            return;
        }

        setUploadStatus('UPLOADING');
        setAnalysisStage('CAPTURE_RECEIVED');

        try {
            const data = await apiClient.uploadPcap(file);
            
            setUploadStatus('ANALYZING');
            
            // Target timings:
            // Capture Received: ~600ms
            // Capture Verified: ~800ms
            // IPsec Analysis: ~1100ms
            // Traffic Analysis: ~1000ms
            // Security Assessment: ~900ms
            // Report Generated: ~700ms

            const pipelineSteps: { stage: AnalysisStage, duration: number }[] = [
                { stage: 'CAPTURE_RECEIVED', duration: 600 },
                { stage: 'CAPTURE_VERIFIED', duration: 800 },
                { stage: 'IPSEC_ANALYSIS', duration: 1100 },
                { stage: 'TRAFFIC_ANALYSIS', duration: 1000 },
                { stage: 'SECURITY_ASSESSMENT', duration: 900 },
                { stage: 'REPORT_GENERATED', duration: 700 }
            ];

            for (const step of pipelineSteps) {
                setAnalysisStage(step.stage);
                await new Promise(r => setTimeout(r, step.duration));
            }
            
            setUploadStatus('SUCCESS');
            setScenario(data);
            navigate('/app/overview');
            
        } catch (err: any) {
            const msg = err.message || '';
            if (msg.includes('not part of the validated capture library')) {
                setUploadError({
                    title: 'CAPTURE NOT RECOGNIZED',
                    message: 'This capture is not part of the validated analysis library. The application could not associate this PCAP with a known analysis profile.'
                });
            } else {
                setUploadError({
                    title: 'ANALYSIS UNAVAILABLE',
                    message: 'The capture could not be processed.'
                });
            }
            setUploadStatus('ERROR');
        } finally {
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const recentCaptures = captures.filter(c => ['S02', 'S06'].includes(c.id));
    const libraryCaptures = captures.filter(c => !['S02', 'S06'].includes(c.id));

    return (
        <div className="max-w-6xl mx-auto space-y-8 pb-12">
            <div className="mb-6 border-b border-[#202326] pb-5">
                <div className="text-xs uppercase tracking-widest text-[#636C73] font-medium mb-1">CAPTURES</div>
                <h2 className="text-2xl font-semibold text-[#E5E7EB] tracking-wide mb-1">Capture Library</h2>
                <p className="text-sm text-[#8B9299]">Manage and analyze IPsec packet captures</p>
            </div>

            {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs px-4 py-3 rounded-sm">
                    {error}
                </div>
            )}

            {/* Upload Area */}
            <div>
                <SectionHeader title="Upload / Ingest" subtitle="Analyze an IPsec packet capture" />
                
                <div className="mt-3">
                    {uploadStatus === 'ERROR' && uploadError ? (
                        <ErrorState 
                            title={uploadError.title} 
                            message={uploadError.message} 
                            onAction={resetUploadState}
                            actionLabel="Try Another Capture"
                        />
                    ) : uploadStatus === 'UPLOADING' || uploadStatus === 'ANALYZING' ? (
                        <div aria-live="polite"><AnalysisPipeline currentStage={analysisStage} filename={selectedFilename} /></div>
                    ) : (
                        <div className="border border-dashed border-[#202326] bg-[#0D0F10] hover:bg-[#101213] rounded-sm p-10 flex flex-col items-center justify-center transition-colors">
                            <input 
                                type="file" 
                                ref={fileInputRef} 
                                className="hidden" 
                                accept=".pcap,.pcapng" 
                                onChange={handleFileUpload} 
                            />
                            <div className="w-12 h-12 bg-[#202326] rounded-full flex items-center justify-center mb-4">
                                <span className="text-[#8B9299] text-lg">↑</span>
                            </div>
                            <h3 className="text-[#E5E7EB] text-sm font-medium mb-1">Upload Capture</h3>
                            <p className="text-[#8B9299] text-xs mb-6 text-center max-w-sm">Drag and drop a PCAP file here, or click to browse your files.</p>
                            <div className="text-[#636C73] text-xs mb-6">or</div>
                            <button 
                                onClick={() => fileInputRef.current?.click()}
                                disabled={isLoading}
                                className="bg-[#202326] hover:bg-[#32363b] text-[#E5E7EB] text-xs px-6 py-2 rounded-sm transition-colors disabled:opacity-50 tracking-wide"
                            >
                                Choose file
                            </button>
                            <div className="flex gap-6 mt-6 text-xs text-[#636C73] uppercase tracking-widest">
                                <span>Supported: .pcap, .pcapng</span>
                                <span>Maximum: 50 MB</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Recent Captures */}
            <div>
                <SectionHeader title="Recent Captures" subtitle="Recently analyzed captures" />
                <div className="mt-3 bg-[#0D0F10] border border-[#202326] rounded-sm overflow-hidden">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-[#202326] bg-[#080909]">
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Capture</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Status</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Packets</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Duration</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">IPsec</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">IKE</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Risk</th>
                                <th className="py-2.5 px-4 text-xs uppercase tracking-widest text-[#636C73] font-medium whitespace-nowrap">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentCaptures.map(c => (
                                <tr key={c.id} className="border-b border-[#101213] hover:bg-[#101213] transition-colors cursor-pointer" onClick={() => handleSelect(c.id)}>
                                    <td className="py-3 px-4 font-mono text-[#3b82f6] text-sm">{c.filename}</td>
                                    <td className="py-3 px-4">
                                        <span className="text-xs uppercase tracking-widest text-[#8B9299] bg-[#202326] px-2 py-0.5 rounded-sm">{c.analysis_status}</span>
                                    </td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E5E7EB]">{c.packet_count.toLocaleString()}</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E5E7EB]">{c.duration_seconds}s</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E5E7EB]">{c.ipsec_coverage_percent}%</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E5E7EB]">{c.ike_version}</td>
                                    <td className="py-3 px-4 font-mono text-[13px] text-[#E5E7EB]">{c.risk_level}</td>
                                    <td className="py-3 px-4">
                                        <button className="text-sm text-[#3b82f6] uppercase tracking-widest hover:text-white transition-colors" onClick={(e) => { e.stopPropagation(); handleSelect(c.id); }}>Open →</button>
                                    </td>
                                </tr>
                            ))}
                            {recentCaptures.length === 0 && (
                                <tr>
                                    <td colSpan={8} className="py-8 text-center text-xs text-[#636C73]">No recent captures</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Demo Capture Library */}
            <div>
                <SectionHeader title="Demo / Test Capture Library" subtitle="Precomputed analysis dataset" />
                <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                    {libraryCaptures.map(c => (
                        <div key={c.id} className="bg-[#0D0F10] border border-[#202326] hover:border-[#32363b] rounded-sm p-4 transition-colors cursor-pointer flex flex-col justify-between" onClick={() => handleSelect(c.id)}>
                            <div>
                                <div className="flex justify-between items-start mb-2">
                                    <div className="font-mono text-[#3b82f6] text-xs font-medium">{c.filename}</div>
                                    <div className="text-xs uppercase tracking-widest text-[#636C73]">{c.analysis_status}</div>
                                </div>
                                <div className="text-xs text-[#E5E7EB] mb-3">{c.display_name}</div>
                                
                                <div className="text-xs text-[#636C73] font-mono mb-2 uppercase tracking-wide">
                                    {c.ike_version} · {c.protocol} · {c.encryption} · {c.mode}
                                </div>
                                <div className="flex flex-wrap gap-x-4 gap-y-2 mb-4">
                                    <div className="text-xs text-[#8B9299]"><span className="text-[#636C73] uppercase tracking-widest mr-1">Pkts</span><span className="font-mono">{c.packet_count.toLocaleString()}</span></div>
                                    <div className="text-xs text-[#8B9299]"><span className="text-[#636C73] uppercase tracking-widest mr-1">Dur</span><span className="font-mono">{c.duration_seconds}s</span></div>
                                    <div className="text-xs text-[#8B9299]"><span className="text-[#636C73] uppercase tracking-widest mr-1">IPsec</span><span className="font-mono">{c.ipsec_coverage_percent}%</span></div>
                                    <div className="text-xs text-[#8B9299]"><span className="text-[#636C73] uppercase tracking-widest mr-1">Risk</span><span className={`font-mono ${c.risk_level === 'CRITICAL' || c.risk_level === 'HIGH' ? 'text-red-400' : c.risk_level === 'MEDIUM' ? 'text-amber-400' : 'text-emerald-400'}`}>{c.risk_level}</span></div>
                                </div>
                            </div>
                            <div className="border-t border-[#101213] pt-3 flex justify-between items-center">
                                <div className="text-xs font-mono text-[#636C73] uppercase">{c.ip_version} · {c.protocol}</div>
                                <button className="text-sm uppercase tracking-widest text-[#3b82f6] hover:text-white transition-colors" onClick={(e) => { e.stopPropagation(); handleSelect(c.id); }}>Open Analysis</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
