import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { ScenarioAnalysis } from '../types';

export type UploadStatus = 'IDLE' | 'UPLOADING' | 'ANALYZING' | 'SUCCESS' | 'ERROR';
export type AnalysisStage = 
    | 'CAPTURE_RECEIVED' 
    | 'CAPTURE_VERIFIED' 
    | 'IPSEC_ANALYSIS' 
    | 'TRAFFIC_ANALYSIS' 
    | 'SECURITY_ASSESSMENT' 
    | 'REPORT_GENERATED';

interface AppState {
    currentScenario: ScenarioAnalysis | null;
    isLoading: boolean;
    error: string | null;
    
    uploadStatus: UploadStatus;
    analysisStage: AnalysisStage | null;
    uploadError: { title: string, message: string } | null;

    setScenario: (scenario: ScenarioAnalysis) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
    
    setUploadStatus: (status: UploadStatus) => void;
    setAnalysisStage: (stage: AnalysisStage | null) => void;
    setUploadError: (error: { title: string, message: string } | null) => void;
    resetUploadState: () => void;
}

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [currentScenario, setCurrentScenario] = useState<ScenarioAnalysis | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    
    const [uploadStatus, setUploadStatus] = useState<UploadStatus>('IDLE');
    const [analysisStage, setAnalysisStage] = useState<AnalysisStage | null>(null);
    const [uploadError, setUploadError] = useState<{ title: string, message: string } | null>(null);

    const setScenario = (scenario: ScenarioAnalysis) => {
        setCurrentScenario(scenario);
        setError(null);
    };

    const resetUploadState = () => {
        setUploadStatus('IDLE');
        setAnalysisStage(null);
        setUploadError(null);
    };

    return (
        <AppContext.Provider value={{
            currentScenario,
            isLoading,
            error,
            uploadStatus,
            analysisStage,
            uploadError,
            setScenario,
            setLoading: setIsLoading,
            setError,
            setUploadStatus,
            setAnalysisStage,
            setUploadError,
            resetUploadState
        }}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};
