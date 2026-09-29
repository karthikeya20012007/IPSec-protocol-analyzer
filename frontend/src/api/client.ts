import type { ScenarioAnalysis, CaptureMetadata } from '../types';

const API_BASE = 'http://localhost:8000/api';

export const apiClient = {
    getScenarios: async (): Promise<CaptureMetadata[]> => {
        const response = await fetch(`${API_BASE}/scenarios`);
        if (!response.ok) throw new Error('Failed to fetch scenarios');
        return response.json();
    },

    analyzeScenario: async (scenarioId: string): Promise<ScenarioAnalysis> => {
        const response = await fetch(`${API_BASE}/analyze/${scenarioId}`);
        if (!response.ok) throw new Error('Failed to fetch scenario analysis');
        return response.json();
    },

    uploadPcap: async (file: File): Promise<ScenarioAnalysis> => {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        return response.json();
    }
};
