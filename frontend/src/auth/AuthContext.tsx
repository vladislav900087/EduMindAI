
import {
    createContext,
    useContext,
    useEffect,
    useMemo,
    useState,
    type ReactNode
    } from 'react';

import { getCurrentUser, loginUser, registerUser } from '../api/authApi';
import type { LoginRequest, RegisterRequest, User } from '../types/auth';


type AuthContextValue = {

    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (data: LoginRequest) => Promise<void>;
    register: (data: RegisterRequest) => Promise<void>;
    logout: () => void;

    };

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {

    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {

        async function loadUser() {

            const token = localStorage.getItem('access_token');

            if (!token) {
                setIsLoading(false);
                return;

                }

            try {

                const currentUser = await getCurrentUser();
                setUser(currentUser);


                } catch {
                    localStorage.removeItem('access_token');
                    setUser(null);

                    } finally {
                        setIsLoading(false);

                        }
            }

        loadUser();


        }, []);

    async function login(data: LoginRequest) {

        const token = await loginUser(data);

        localStorage.setItem('access_token', token.access_token);

        const currentUser = await getCurrentUser();
        setUser(currentUser);

        }

    async function register(data: RegisterRequest) {

        await registerUser(data);

        await login({
            email: data.email,
            password: data.password,
            });

        }

    function logout() {

        localStorage.removeItem('access_token');
        setUser(null);

        }

    const value = useMemo<AuthContextValue>(

        () => ({
            user,
            isLoading,
            isAuthenticated: user !== null,
            login,
            register,
            logout,
            }),
        [user, isLoading],

        );

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;


    }

export function useAuth() {

    const context = useContext(AuthContext);

    if (context === undefined) {

        throw new Error('useAuth must be used inside AuthProvider');

        }

    return context;
    }
