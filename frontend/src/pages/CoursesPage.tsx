import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { createCourse, getCourses, getMyCourses, publishCourse } from '../api/coursesApi';
import CourseForm from '../components/courses/CourseForm';
import Button from '../components/ui/Button';
import { useAuth } from '../auth/AuthContext';
import type { Course } from '../types/course';
import { useTranslation } from 'react-i18next';

import { formatCoursePrice } from '../utils/money';



function CoursesPage() {

    const { user } = useAuth();
    const { t } = useTranslation();

    const [courses, setCourses] = useState<Course[]>([]);
    const [myCourses, setMyCourses] = useState<Course[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    const canManageCourses = user?.role === 'teacher' || user?.role === 'admin';


    async function loadCourses() {

            setErrorMessage('');

            try {
                const courseData = await getCourses();
                setCourses(courseData);

                if (canManageCourses) {

                    const myCourseData = await getMyCourses();
                    setMyCourses(myCourseData);

                    }

                } catch {

                    setErrorMessage(t('courses.loadError'));

                    } finally {
                        setIsLoading(false);

                    }

    }

    useEffect(() => {
        loadCourses();
        }, [canManageCourses]);


    async function handleCreateCourse(values: {

        title: string;
        description: string;
        price_amount: number;
        currency: 'KZT' | 'EUR';

        }) {

            const createdCourse = await createCourse({

                title: values.title,
                description: values.description || null,
                price_amount: values.price_amount,
                currency: values.currency,


                });

            setMyCourses((currentCourses) => [createdCourse, ...currentCourses]);



            }

    async function handlePublishCourse(courseId: number) {

        const updatedCourse = await publishCourse(courseId);

        setMyCourses((currentCourses) => currentCourses.map((course) =>
            course.id === updatedCourse.id ? updatedCourse : course,


            ),
        );

        setCourses((currentCourses) => {

            const alreadyListed = currentCourses.some(
                (course) => course.id === updatedCourse.id,
                );

            if (alreadyListed) {
                return currentCourses.map((course) =>
                    course.id === updatedCourse.id
                        ? updatedCourse
                        : course,
                );
            }

            return [updatedCourse, ...currentCourses];
            });

     }

    return (

        <section>
            <div className='flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between'>
                <div>
                    <p className='text-sm font-medium text-blue-600'>{t('courses.title')}</p>
                    <h1 className='mt-2 text-2xl font-semibold text-slate-900'>{t('courses.catalog')}</h1>
                    <p className='mt-2 text-slate-600'>{t('courses.description')}</p>
                </div>
            </div>

            {isLoading && (
                <div className='mt-8 rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>{t('courses.loading')}</div>

                )}

            {errorMessage && (
                <div className='mt-8 rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                    {errorMessage}
                </div>
                )}

            {!isLoading && !errorMessage && canManageCourses && (
                <div className='mt-8 grid gap-6 lg:grid-cols-[360px_1fr]'>
                    <CourseForm
                        defaultCurrency={user?.region === 'europe' ? 'EUR' : 'KZT'}
                        onSubmit={handleCreateCourse}

                        />

                    <section>
                        <h2 className='text-lg font-semibold text-slate-900'>
                            {t('courses.mine')}
                        </h2>

                        {myCourses.length === 0 ? (
                            <div className='mt-4 rounded-lg border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-600 shadow-sm'>
                                {t('courses.noneMine')}
                            </div>

                            ) : (
                                <div className='mt-4 space-y-3'>
                                    {myCourses.map((course) => (

                                        <div
                                            key={course.id}
                                            className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'
                                        >
                                            <div className='flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between'>
                                                <div>
                                                    <div className='flex items-center gap-2'>
                                                        <span className='rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium capitalize text-blue-700'>
                                                            {course.status}
                                                        </span>
                                                        <span className='text-xs text-slate-500'>
                                                            #{course.id}
                                                        </span>

                                                    </div>
                                                    <h3 className='mt-3 text-lg font-semibold text-slate-950'>
                                                        {course.title}
                                                    </h3>
                                                    <p className='mt-2 text-sm text-slate-600'>
                                                        {course.description || t('common.noDescription')}
                                                    </p>
                                                    <p className='mt-3 text-sm font-semibold text-slate-900'>
                                                        {formatCoursePrice(course.price_amount, course.currency)}
                                                    </p>
                                                </div>
                                                <div className='flex shrink-0 gap-2'>
                                                    <Link
                                                        className='rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100'
                                                        to={`/courses/${course.id}`}
                                                    >
                                                        {t('common.open')}
                                                    </Link>

                                                    {course.status === 'draft' && (
                                                        <Button
                                                            type='button'
                                                            onClick={() => handlePublishCourse(course.id)}
                                                        >
                                                            {t('common.publish')}
                                                        </Button>

                                                        )}
                                                </div>
                                            </div>
                                        </div>
                                        ))}
                                </div>

                                )}
                    </section>
                </div>
              )}

            {!isLoading && !errorMessage && (
                <section className='mt-10'>
                    <h2 className='text-lg font-semibold text-slate-900'>
                        {t('courses.all')}
                    </h2>

                    {courses.length === 0 ? (
                        <div className='mt-4 rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm'>
                            <h3 className='text-lg font-semibold text-slate-900'>
                                {t('courses.none')}
                            </h3>
                            <p>
                                {t('courses.publishedHere')}
                            </p>
                        </div>

                        ) : (
                            <div className='mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3'>
                             {courses.map((course) => (
                                 <Link
                                    key={course.id}
                                    to={`/courses/${course.id}`}
                                    className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md'
                                 >
                                    <div className='flex items-center justify-between gap-3'>
                                        <span className='rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium capitalize text-blue-700'>
                                            {course.status}
                                        </span>
                                        <span className='text-xs text-slate-500'>
                                            #{course.id}
                                        </span>
                                    </div>
                                    <h3 className='mt-4 text-lg font-semibold text-slate-950'>
                                        {course.title}
                                    </h3>
                                    <p className='mt-2 text-sm text-slate-600'>
                                        {course.description || t('common.noDescription')}
                                    </p>
                                    <div className='mt-5 text-sm font-medium text-blue-600'>
                                        {t('courses.openCourse')}
                                    </div>
                                 </Link>
                                 ))}
                            </div>
                            )}
                </section>
                )}
            </section>
        );
    }

export default CoursesPage;
