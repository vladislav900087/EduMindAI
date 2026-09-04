import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

import { getCourse } from '../api/coursesApi';
import type { Course } from '../types/course';


function CourseDetailPage() {

    const { courseId } = useParams();

    const [course, setCourse] = useState<Course | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {

        async function loadCourse() {

            if (!courseId) {

                setErrorMessage('Course id is missing.');
                setIsLoading(false);
                return;


                }

            try {

                const data = await getCourse(Number(courseId));
                setCourse(data);

                } catch {

                    setErrorMessage('Could not load course.');


                    } finally {

                        setIsLoading(false);

                        }
            }

        loadCourse();
        }, [courseId]);


    if (isLoading) {

        return (
            <section className='rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>
                Loading course...
            </section>

            );

        }

    if (errorMessage || !course) {

        return (
            <section className='rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                {errorMessage || 'Course not found.'}
            </section>


            );

        }


    return (
        <section>
            <Link className='text-sm font-medium text-blue-600 hover:text-blue-700' to='/courses'>
                Back to courses
            </Link>

            <div className='mt-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'>
                <div className='flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between'>
                    <div>
                        <p className='text-sm font-medium text-blue-600'>Course</p>
                        <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
                            {course.title}
                        </h1>
                        <p className='mt-3 max-w-3xl text-slate-600'>
                            {course.description || 'No description provided.'}
                        </p>
                    </div>

                    <span className='w-fit rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium capitalize text-blue-700'>
                        {course.status}
                    </span>

                </div>
            </div>

            <div className='mt-6 grid gap-4 md:grid-cols-3'>
                <div className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <h2 className='font-semibold text-slate-900'>Lessons</h2>
                    <p className='mt-2 text-sm text-slate-600'>
                        Course lessons will appear here.
                    </p>
                </div>

                <div className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <h2 className='font-semibold text-slate-900'>Quizzes</h2>
                    <p className='mt-2 text-sm text-slate-600'>Course quizzes will appear here.</p>
                </div>

                <div className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <h2 className='font-semibold text-slate-900'>Assignments</h2>
                    <p className='mt-2 text-sm text-slate-600'>Course assignments will appear here.</p>
                </div>
            </div>
        </section>
        );
    }

export default CourseDetailPage;