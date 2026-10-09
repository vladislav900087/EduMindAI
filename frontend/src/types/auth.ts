export type UserRole = "student" | "admin" | "teacher";
export type UserRegion = 'europe' | 'kazakhstan';
export type InterfaceLanguage = 'en' | 'ru' | 'de' | 'kk'


export type User = {
    id: number;
    email: string;
    full_name: string;
    role: UserRole;
    region: UserRegion;
    language: InterfaceLanguage;
    created_at: string;

    };

export type UserPreferencesUpdate = {
    region: UserRegion;
    language: InterfaceLanguage;
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

