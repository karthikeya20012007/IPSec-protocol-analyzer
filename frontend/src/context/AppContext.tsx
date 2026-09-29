import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { ScenarioAnalysis } from '../types';

interface AppState {
    currentScenario: ScenarioAnalysis | null;
    isLoading: boolean;
    error: string | null;
    setScenario: (scenario: ScenarioAnalysis) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
}

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [currentScenario, setCurrentScenario] = useState<ScenarioAnalysis | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const setScenario = (scenario: ScenarioAnalysis) => {
        setCurrentScenario(scenario);
        setError(null);
    };

    return (
        <AppContext.Provider value={{
            currentScenario,
            isLoading,
            error,
            setScenario,
            setLoading: setIsLoading,
            setError
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
