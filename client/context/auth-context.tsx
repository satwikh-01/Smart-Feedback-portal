"use client";

import React, { createContext, useState, useContext, useEffect, ReactNode, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from "sonner";
import { User, AuthContextType } from '@/types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the backend API URL.
const API_URL = "http://localhost:8000/api/v1";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    const fetchUser = useCallback(async (authToken: string) => {
        try {
            // Note: We will need to create this /api/v1/users/me endpoint in the backend.
            const response = await fetch(`${API_URL}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                },
            });

            if (!response.ok) {
                throw new Error("Session expired or invalid.");
            }

            const userData: User = await response.json();
            setUser(userData);

        } catch (error) {
            console.error("Failed to fetch user:", error);
            logout(); // If we can't fetch the user, log them out.
        }
    }, []);

    useEffect(() => {
        const initializeAuth = async () => {
            const storedToken = localStorage.getItem('authToken');
            if (storedToken) {
                setToken(storedToken);
                await fetchUser(storedToken);
            }
            setIsLoading(false);
        };
        initializeAuth();
    }, [fetchUser]);

    const login = async (data: any) => {
        try {
            // The backend expects form data for the login endpoint
            const formData = new URLSearchParams();
            formData.append('username', data.email);
            formData.append('password', data.password);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to log in.");
            }

            const session = await response.json();
            const authToken = session.access_token;

            setToken(authToken);
            localStorage.setItem('authToken', authToken);

            await fetchUser(authToken);

            toast.success("Login successful!");
            router.push('/'); // Redirect to dashboard after login

        } catch (error: any) {
            toast.error(error.message || "An unexpected error occurred.");
        }
    };

    const register = async (data: any) => {
        try {
            // Construct a clean payload based on the user's role
            const payload: any = {
                email: data.email,
                full_name: data.full_name,
                password: data.password,
                role: data.role,
            };

            if (data.role === 'manager') {
                payload.team_name = data.team_name;
            } else if (data.role === 'employee') {
                payload.team_id = data.team_id;
            }

            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to register.");
            }

            toast.success("Registration successful! Please log in.");
            router.push('/login'); // Redirect to login page after successful registration

        } catch (error: any) {
            toast.error(error.message || "An unexpected error occurred.");
        }
    };

    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('authToken');
        router.push('/login'); // Redirect to login page on logout
    };

    const value = {
        user,
        token,
        isLoading,
        login,
        register,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
