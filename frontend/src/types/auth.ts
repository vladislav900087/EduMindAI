export type UserRole = "student" | "admin" | "teacher";


export type User = {
    id: number;
    email: string;
    full_name: string;
    role: UserRole;
    created_at: string;

    };

export type RegisterRequest = {
    email: string;
    full_name: string;
    password: string;

    };

export type LoginRequest = {

    email: string;
    password: string;

    };

export type TokenResponse = {
    access_token: string;
    token_type: string;

    };

