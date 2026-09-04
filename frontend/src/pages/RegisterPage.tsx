import { type FormEvent, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';

import { useAuth } from '../auth/AuthContext';

function RegisterPage() {

    const navigate = useNavigate();
    const { isAuthenticated, register } = useAuth();

    const [fullName, setFullName] = useState('');
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
            await register({email, full_name: fullName, password});
            navigate('/dashboard');


            } catch {
                setErrorMessage('Could not create account. Try another email')

                } finally {

                    setIsSubmitting(false);

                    }


        }




    return (
        <main className='flex min-h-screen items-center justify-center bg-slate-50 px-6'>
            <section className='w-full max-w-md rounded-lg border border-slate-200 bg-white p-8 shadow-sm'>
                <p className='text-sm font-medium text-blue-600'>EduMindAI</p>
                <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Create account</h1>
                <p className='mt-2 text-sm text-slate-600'>Join EduMindAI as a student or teacher.</p>


                <form className='mt-6 space-y-4' onSubmit={handleSubmit}>
                    <label className='block'>
                        <span className='text-sm font-medium text-slate-700'>Full name</span>
                        <input
                            className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                            type='text'
                            value={fullName}
                            onChange={(event) => setFullName(event.target.value)}
                            required
                         />

                    </label>

                    <label className='block'>
                        <span className='text-sm font-medium text-slate-700'>Email</span>
                        <input
                            className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                            type='email'
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
                            minLength={6}

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
                        {isSubmitting ? "Creating account..." : "Create account"}

                    </button>
                </form>

                <p className='mt-5 text-center text-sm text-slate-600'>
                    Already have an account?{" "}
                    <Link className='font-medium text-blue-600 hover:text-blue-700' to='/login'>
                        Sign In
                    </Link>
                </p>
            </section>
        </main>



        );


    }

export default RegisterPage;