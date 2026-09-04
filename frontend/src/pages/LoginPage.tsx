import { type FormEvent, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';

import { useAuth } from '../auth/AuthContext';

function LoginPage() {

    const navigate = useNavigate();
    const { isAuthenticated, login } = useAuth();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    if (isAuthenticated) {

        return <Navigate to='/dashboard' replace />;

        }

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {

        event.preventDefault();

        setErrorMessage('');
        setIsSubmitting(true);

        try {
            await login({ email, password });
            navigate('/dashboard');
            } catch {
                setErrorMessage('Invalid email or password.');

                } finally {
                    setIsSubmitting(false);

                    }
        }


    return (
        <main className='flex min-h-screen items-center justify-center bg-slate-50 px-6'>
            <section className='w-full max-w-md rounded-lg border border-slate-200 bg-white p-8 shadow-sm'>
                <p className='text-sm font-medium text-blue-600'>EduMindAI</p>
                <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Sign in</h1>
                <p className='mt-2 text-sm text-slate-600'>Access your courses, lessons, quizzes, and assignments</p>

                <form className='mt-6 space-y-4' onSubmit={handleSubmit}>
                    <label className='block'>
                        <span className='text-sm font-medium text-slate-700'>Email</span>
                        <input
                            className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                         />
                    </label>

                    <label className='block'>
                        <span className='text-sm font-medium text-slate-700'>Password</span>
                        <input
                            className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                            type='password'
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            required

                         />
                    </label>

                    {errorMessage && (
                        <p className='rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                            {errorMessage}
                        </p>

                        )}

                    <button
                        className='w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300'
                        type='submit'
                        disabled={isSubmitting}

                    >
                        {isSubmitting ? "Signing in..." : "Sign in"}
                    </button>
                </form>

                <p className="mt-5 text-center text-sm text-slate-600">
                    No account?{" "}
                    <Link className='font-medium text-blue-600 hover:text-blue-700' to='/register'>Create one</Link>
                </p>

            </section>

        </main>
        );
    }

export default LoginPage;