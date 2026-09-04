import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from '../../auth/AuthContext';


const navItems = [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/courses", label: "Courses" },
    { to: "/assignments", label: "Assignments" },

    ];

function AppLayout() {

    const navigate = useNavigate();
    const { user, logout } = useAuth();

    function handleLogout() {

        logout();
        navigate('/login');

        }

    return (
        <div className='min-h-screen bg-slate-50 text-slate-900'>
            <aside className='fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white px-5 py-6 md:block'>
                <div>
                    <p className='text-sm font-medium text-blue-600'>EduMindAI</p>
                    <h1 className='mt-1 text-lg font-semibold text-slate-950'>Learning Portal</h1>
                </div>

                <nav className='mt-8 space-y-1'>
                    {navItems.map((item) => (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            className={({ isActive }) => [

                                    "block rounded-md px-3 py-2 text-sm font-medium",
                                    isActive ? 'bg-blue-50 text-blue-700' : "text-slate-600 hover:bg-slate-100 hover:text-slate-950",


                                ].join(" ")
                            }
                        >
                            {item.label}
                        </NavLink>

                        ))}
                </nav>
            </aside>

            <div className="md:pl-64">
                <header className='border-b border-slate-200 bg-white px-6 py-4'>
                    <div className='mx-auto flex max-w-6xl items-center justify-between'>
                        <span className='text-sm font-medium text-slate-600'>EduMindAI</span>
                        <div className='flex items-center gap-3'>
                            <div className='text-right'>
                                <p className='text-sm font-medium text-slate-900'>{user?.full_name}</p>
                                <p className='text-xs capitalize text-slate-500'>{user?.role}</p>
                            </div>

                            <button
                                className='rounded-md border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100'
                                type='button'
                                onClick={handleLogout}
                            >Log out</button>
                        </div>
                    </div>

                </header>

                <main className="mx-auto max-w-6xl px-6 py-8">
                    <Outlet />
                </main>
            </div>
        </div>
        );
    }

export default AppLayout;