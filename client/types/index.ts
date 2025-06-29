export type UserRole = "manager" | "employee";

export interface User {
    id: number;
    email: string;
    full_name: string;
    role: UserRole;
    team_id?: number | null;
}

export interface Comment {
    id: number;
    content: string;
    created_at: string;
    user: User;
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
