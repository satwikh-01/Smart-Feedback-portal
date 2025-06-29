import { useAuth } from '@/context/auth-context';
import { useCallback } from 'react';
import { toast } from 'sonner';
import { Team } from '@/types';

const API_URL = "http://localhost:8000/api/v1";

// Unauthenticated API fetch function
const unauthenticatedApiFetch = async (
    endpoint: string,
    options: RequestInit = {},
    responseType: 'json' | 'blob' = 'json'
) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "An unknown API error occurred" }));
        throw new Error(errorData.detail || 'An API error occurred');
    }

    if (responseType === 'blob') {
        return response.blob();
    }

    if (response.status === 204) {
        return true;
    }

    return response.json();
};

// Custom hook for making authenticated API calls
export function useApi() {
    const { token, logout } = useAuth();

    const apiFetch = useCallback(async (
        endpoint: string,
        options: RequestInit = {},
        responseType: 'json' | 'blob' = 'json'
    ) => {
        if (!token) {
            return null;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (response.status === 401) {
            toast.error("Your session has expired. Please log in again.");
            logout();
            return null;
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "An unknown API error occurred" }));
            throw new Error(errorData.detail || 'An API error occurred');
        }

        if (responseType === 'blob') {
            return response.blob();
        }

        if (response.status === 204) {
            return true;
        }

        return response.json();
    }, [token, logout]);

    const getTeams = useCallback(async (): Promise<Team[]> => {
        try {
            const data = await unauthenticatedApiFetch('/teams/');
            return data as Team[];
        } catch (error) {
            toast.error('Failed to fetch teams. Please try again later.');
            return [];
        }
    }, []);

    return { apiFetch, getTeams };
}
