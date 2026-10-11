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
import { useTranslation } from 'react-i18next';

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

    const { t } = useTranslation();


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
                    setErrorMessage(t('dashboard.loadError'));
                    } finally {
                        setIsLoading(false);
                        }
            }
        loadDashboard();
        }, [isStudent]);

    if (isLoading) {

        return (
            <p className='text-sm text-slate-600'>
                {t('common.loading')}
            </p>
            );

        }



    return (
        <section>
            <p className='text-sm font-medium text-blue-600'>
                {t('dashboard.overview')}
            </p>

            <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
                {t('dashboard.welcome', { name: user?.full_name })}
            </h1>

            <p className='mt-2 text-slate-600'>
                {isStudent ? t('dashboard.studentDescription') : t('dashboard.teacherDescription')}
            </p>

            {errorMessage && (
                <p className='mt-6 rounded-md bg-red-50 p-4 text-sm text-red-700'>
                    {errorMessage}
                </p>
                )}

            {!errorMessage && isStudent && (
                <>
                    <div className='mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4'>
                        <Stat label={t('dashboard.enrolledCourses')} value={stats.courses} />
                        <Stat
                            label={t('dashboard.submittedAssignments')}
                            value={stats.assignments}
                        />
                        <Stat
                            label={t('dashboard.gradedAssignments')}
                            value={stats.gradedAssignments}
                        />
                        <Stat
                            label={t('dashboard.averageQuizScore')}
                            value={`${stats.averageQuizScore}%`}
                        />
                    </div>

                    <div className='mt-8 flex flex-wrap gap-3'>
                        <Link
                            to='/courses'
                            className='rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700'
                         >
                            {t('dashboard.continueLearning')}
                         </Link>

                         <Link
                            to='/assignments'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                         >
                            {t('dashboard.viewAssignments')}
                         </Link>

                         <Link
                            to='/quiz-history'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                         >
                            {t('nav.quizHistory')}
                         </Link>
                    </div>

                </>
                )}

            {!errorMessage && !isStudent && (
                <>
                    <div className='mt-8 grid gap-4 sm:grid-cols-3'>
                        <Stat label={t('dashboard.myCourses')} value={stats.courses} />
                        <Stat
                            label={t('dashboard.assignments')}
                            value={stats.assignments}
                         />
                         <Stat
                            label={t('dashboard.awaitingGrading')}
                            value={stats.submissionsToGrade}
                         />
                    </div>

                    <div className='mt-8 flex flex-wrap gap-3'>
                        <Link
                            to='/courses'
                            className='rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700'
                        >
                            {t('dashboard.manageCourses')}
                        </Link>

                        <Link
                            to='/assignments'
                            className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                        >
                            {t('dashboard.reviewAssignments')}
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
