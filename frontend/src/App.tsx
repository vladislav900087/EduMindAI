import { Navigate, Route, Routes } from 'react-router-dom';

import AppLayout from './components/layout/AppLayout';
import AssignmentDetailPage from './pages/AssignmentDetailPage';
import AssignmentsPage from './pages/AssignmentsPage';
import CourseDetailPage from './pages/CourseDetailPage';
import CoursesPage from './pages/CoursesPage';
import QuizTakingPage from './pages/QuizTakingPage';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage'

import ProtectedRoute from './auth/ProtectedRoute';


function App() {

    return (
        <Routes>
            <Route path='/' element={<Navigate to='/dashboard' replace />} />
            <Route path='/login' element={<LoginPage />} />
            <Route path='/register' element={<RegisterPage />} />

            <Route element={<ProtectedRoute />}>
                <Route element={<AppLayout />}>
                    <Route path='/dashboard' element={<DashboardPage />} />
                    <Route path='/courses' element={<CoursesPage />} />
                    <Route path='/courses/:courseId' element={<CourseDetailPage />} />
                    <Route path='/assignments' element={<AssignmentsPage />} />
                    <Route path='/assignments/:assignmentId' element={<AssignmentDetailPage />} />
                    <Route path='/quizzes/:quizId/take' element={<QuizTakingPage />} />
                </Route>
            </Route>
        </Routes>

        );
    }

export default App;
