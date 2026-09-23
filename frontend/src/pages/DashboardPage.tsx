import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import {
    getAssignmentSubmissions,
    getCourseAssignments,
    getMySubmissions,

    } from '../api/assignmentsApi';

import { getMyCourses } from '../api/coursesApi';
import {getMyEnrollments } from '../api/enrollmentsApi';
import { getMyCompletedQuizAttempts} from '../api/quizAttemptsApi';
import { useAuth } from '../auth/AuthContext';

type DashboardStats = {
    courses: number;
    assignments: number;
    gradedAssignments: number;
    quizAttempts: number;
    averageQuizScore: number;
    submissionsToGrade: number;
    };

const emptyStats: DashboardStats = {
    courses: 0,
    assignments: 0,
    gradedAssignments: 0,
    quizAttempts: 0,
    averageQuizScore: 0,
    submissionsToGrade: 0,
    };



function DashboardPage() {


    const { user } = useAuth();

    const [stats, setStats] = useState<DashboardStats>(emptyStats);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    const isStudent = user?.role === 'student';

    useEffect(() => {

        async function loadDashboard() {
            setIsLoading(true);
            setErrorMessage('');

            try {
                if (isStudent) {
                    const [enrollments, submissions, attempts] = await Promise.all([getMyEnrollments(), getMySubmissions(), getMyCompletedQuizAttempts()]);
                    const averageScore = attempts.length > 0
                     ? attempts.reduce(
                         (total, attempt) =>
                         total + (attempt.score ?? 0),
                         0,
                         ) / attempts.length
                     : 0;

                     setStats({
                         ...emptyStats,
                         courses: enrollments.length,
                         assignments: submissions.length,
                         gradedAssignments: submissions.filter(
                             (submission) => submission.grade !== null,
                             ).length,
                         quizAttempts: attempts.length,
                         averageQuizScore: Math.round(averageScore),
                         });


                    } else {
                        const courses = await getMyCourses();

                        const assignmentsByCourse = await Promise.all(
                            courses.map((course) => getCourseAssignments(course.id),
                            ),
                        );

                        const assignments = assignmentsByCourse.flat();

                        const submissionsByAssignment = await Promise.all(
                            assignments.map((assignment) =>
                                getAssignmentSubmissions(assignment.id),
                            ),
                        );

                        const submissions = submissionsByAssignment.flat();

                        setStats({
                            ...emptyStats,
                            courses: courses.length,
                            assignments: assignments.length,
                            submissionsToGrade: submissions.filter(
                                (submission) => submission.grade === null,
                               ).length,
                            });
                    }
                } catch {
                    setErrorMessage('Could not load dashboard information.');
                    } finally {
                        setIsLoading(false);
                        }
            }
        loadDashboard();
        }, [isStudent]);

    if (isLoading) {

        return (
            <p className='text-sm text-slate-600'>
                Loading dashboard...
            </p>
            );

        }



    return (
        <section>
            <p className='text-sm font-medium text-blue-600'>
                Overview
            </p>

            <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
                Welcome, {user?.full_name}
            </h1>

            <p className='mt-2 text-slate-600'>
                {isStudent ? 'Track your learning and recent results.' : 'Manage your courses and student work.'}
            </p>

            {errorMessage && (
                <p className='mt-6 rounded-md bg-red-50 p-4 text-sm text-red-700'>
                    {errorMessage}
                </p>
                )}

            {!errorMessage && isStudent && (
                <>
                    <div className='mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4'>
                        <Stat label='Enrolled courses' value={stats.courses} />
                        <Stat
                            label='Submitted assignments'
                            value={stats.assignments}
                        />
                        <Stat
                            label='Graded assignments'
                            value={stats.gradedAssignments}
                        />
                        <Stat
                            label='Average quiz score'
                            value={`${stats.averageQuizScore}%`}
                        />
                    </div>

                    <div className='mt-8 flex flex-wrap gap-3'>
                        <Link
                            to='/courses'
                            className='rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700'
                         >
                            Continue learning...
                         </Link>

                         <Link
                            to='/assignments'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                         >
                            View assignments
                         </Link>

                         <Link
                            to='/quiz-history'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                         >
                            Quiz history
                         </Link>
                    </div>

                </>
                )}

            {!errorMessage && !isStudent && (
                <>
                    <div className='mt-8 grid gap-4 sm:grid-cols-3'>
                        <Stat label='My courses' value={stats.courses} />
                        <Stat
                            label='Assignments'
                            value={stats.assignments}
                         />
                         <Stat
                            label='Awaiting grading'
                            value={stats.submissionsToGrade}
                         />
                    </div>

                    <div className='mt-8 flex flex-wrap gap-3'>
                        <Link
                            to='/courses'
                            className='rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700'
                        >
                            Manage courses
                        </Link>

                        <Link
                            to='/assignments'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                        >
                            Review assignments
                        </Link>
                    </div>
                </>
                )}
        </section>

        );
    }

function Stat({
    label,
    value,
    }: {
        label: string;
        value: number | string;
        }) {
            return (
                <div className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <p className='text-sm text-slate-600'>
                        {label}
                    </p>
                    <p className='mt-2 text-3xl font-semibold text-slate-950'>
                        {value}
                    </p>
                </div>
                );
            }

export default DashboardPage;