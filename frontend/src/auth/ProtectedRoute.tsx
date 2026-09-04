import { Navigate, Outlet } from 'react-router-dom';

import { useAuth } from './AuthContext';

function ProtectedRoute() {

    const { isAuthenticated, isLoading } = useAuth();

    if (isLoading) {

        return (
            <main className='flex min-h-screen items-center justify-center bg-slate-50 text-slate-600'>
            Loading...
            </main>

            );

        }

    if (!isAuthenticated) {

        return <Navigate to='/login' replace />;

        }

    return <Outlet />;


    }

export default ProtectedRoute;