import { useParams, Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getLesson, getMyProgress, deleteLesson, completeLesson } from '../api/lessonsApi';
import { getCourse } from '../api/coursesApi';
import { useAuth } from '../auth/AuthContext';
import Button from '../components/ui/Button';
import type { Lesson, LessonProgress } from '../types/lesson';
import type { Course } from '../types/course';
import { getMyEnrollments } from '../api/enrollmentsApi.ts';
import type { Enrollment } from '../types/enrollment';
import axios from 'axios';


function LessonDetailPage() {
    const { t } = useTranslation();

    const { lessonId } = useParams();
    const { user } = useAuth();

    const [lesson, setLesson] = useState<Lesson | null>(null);
    const [lessonCourse, setLessonCourse] = useState<Course | null>(null);
    const [progress, setProgress] = useState<LessonProgress | undefined>(undefined);
    const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [pendingAction, setPendingAction] = useState<'complete' | 'delete' | null>(null);
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [actionError, setActionError] = useState('');

    const isStudent = user?.role === 'student';
    const isEnrolled = enrollments.some(
        (enrollment) => enrollment.course_id === lesson?.course_id
        );




    const isCompleted = progress?.lesson_id === lesson?.id;


    const canManageLesson = user?.role === 'admin' || (
            user?.role === 'teacher' &&
            lessonCourse !== null &&
            lessonCourse.teacher_id === user.id

        );

    const navigate = useNavigate();




    useEffect(() => {

            let cancelled = false;

            async function loadLessonData() {
                setIsLoading(true);
                setErrorMessage('');
                setActionError('');
                setLesson(null);
                setLessonCourse(null);
                setProgress(undefined);
                setEnrollments([]);

                if (!lessonId) {

                        setErrorMessage(t('learning.lessonIdMissing'));
                        setIsLoading(false);
                        return;
                    }

                const id = Number(lessonId);

                if (!Number.isInteger(id) || id <= 0) {
                    setErrorMessage(t('learning.invalidLessonId'));
                    setIsLoading(false);
                    return;
                    }

                try {

                    const lessonData = await getLesson(id);

                    if (cancelled) return;

                    setLesson(lessonData);

                    const courseData = await getCourse(lessonData.course_id);

                    if (cancelled) return;

                    setLessonCourse(courseData);

                    if (user?.role === 'student') {

                        const enrollmentData = await getMyEnrollments();

                        if (cancelled) return;

                        setEnrollments(enrollmentData);

                        const enrolled = enrollmentData.some(
                            (enrollment) => enrollment.course_id === courseData.id,
                            );

                        if (!enrolled) return;

                        const progressData = await getMyProgress();

                        if (cancelled) return;

                        setProgress(
                            progressData.find((item) => item.lesson_id === lessonData.id),
                            );



                        }

                    } catch (error: unknown) {

                            if (cancelled) return;

                            if (axios.isAxiosError(error)) {

                                    const detail = error.response?.data?.detail;

                                    setErrorMessage(
                                            typeof detail === 'string'
                                                ? detail
                                                : t('learning.loadLessonError')
                                        );

                                } else {
                                    setErrorMessage(t('learning.loadLessonError'));
                                    }
                                } finally {

                                            if (!cancelled) {
                                                    setIsLoading(false);
                                                }
                                        }
                        }




            void loadLessonData();

            return () => {
                cancelled = true;
                };
        }, [lessonId, user?.id, user?.role]);

    async function handleDeleteLesson() {

        if (!lesson) {
                return;
            }

        setActionError('');
        setPendingAction('delete')

        try {
            await deleteLesson(lesson.id);
            navigate(`/courses/${lesson.course_id}`, {
                replace: true,
                })

            } catch {
                setActionError(t('learning.deleteLessonError'));
                } finally {
                    setPendingAction(null);
                    }
        }

    async function handleCompleteLesson() {

        if (!lesson) {
            return;
            }

        setActionError('');
        setPendingAction('complete');

        try {
            const progress = await completeLesson(lesson.id);
            setProgress(progress);

            } catch {
                setActionError(t('learning.completeError'));
                } finally {
                    setPendingAction(null);
                    }
        }


    if (isLoading) {

        return (
            <section className='rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>
                {t('learning.loadLesson')}
            </section>
            );
        }

    if (errorMessage || !lesson) {

        return (
            <section className='rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                {errorMessage || t('learning.lessonNotFound')}
            </section>
            );
        }


    return (
        <section>
            <Link className='text-sm text-blue-600 hover:text-blue-700' to={`/courses/${lesson.course_id}`}>
                {t('common.backToCourse')}
            </Link>

            <div className='mt-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'>
                <h1 className='mt-4 text-2xl font-semibold text-slate-950'>
                    {lesson.title}
                </h1>

                <p className='mt-3 max-w-3xl text-slate-600 mb-10'>
                    {lesson.content || t('learning.noContent')}
                </p>

                {isStudent && isEnrolled && (
                    <div className='mt-5 border-t border-slate-100 pt-5'>
                        {isCompleted ? (
                            <div>
                                <span className='rounded-md bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700'>
                                    {t('learning.completed')}
                                </span>

                            </div>
                            ) : (
                                    <Button type='button' onClick={handleCompleteLesson}>
                                        {
                                            pendingAction === 'complete'
                                                ? t('learning.completing')
                                                : t('learning.completeLesson')
                                            }
                                    </Button>
                                )}


                        </div>

                    )}

                {actionError && (
                                <p className='mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                                    {actionError}
                                </p>
                                )}

                {canManageLesson && (
                    <Button type='button' onClick={handleDeleteLesson}>
                        {
                            pendingAction === 'delete'
                                ? t('learning.deleting')
                                : t('learning.deleteLesson')
                            }
                    </Button>
                    )}




            </div>
        </section>
        );
    }

export default LessonDetailPage;
