export type UserRole = "manager" | "employee";

export interface User {
    id: string;
    email: string;
    full_name: string;
    role: "manager" | "employee";
    team_id?: number;
}

export interface Notification {
    id: number;
    message: string;
    is_read: boolean;
    created_at: string;
}


export interface AuthContextType {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    login: (data: any) => Promise<void>;
    register: (data: any) => Promise<void>;
    logout: () => void;
}

export interface Team {
    id: number;
    name: string;
}

export interface Tag {
    id: number;
    name: string;
}

export interface Feedback {
    id: number;
    strengths: string;
    areas_for_improvement: string;
    sentiment: 'positive' | 'neutral' | 'negative';
    feedback: string;
    acknowledged: boolean;
    created_at: string;
    employee: User;
    manager?: User;
    tags: Tag[];
}
