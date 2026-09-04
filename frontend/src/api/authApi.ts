import { apiClient } from './client';
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types/auth';


export async function registerUser(data: RegisterRequest): Promise<User> {

    const response = await apiClient.post<User>("/auth/register", data);

    return response.data;


    }

export async function loginUser(data: LoginRequest): Promise<TokenResponse> {

    const formData = new URLSearchParams();

    formData.append("username", data.email);
    formData.append("password", data.password)

    const response = await apiClient.post<TokenResponse>('/auth/login', formData, {
        headers: {'Content-Type': "application/x-www-form-urlencoded",
            },
        });

    return response.data;

    }

export async function getCurrentUser(): Promise<User> {

    const response = await apiClient.get<User>('/users/me');

    return response.data;

    }