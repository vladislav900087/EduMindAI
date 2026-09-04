import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { getCourses } from '../api/coursesApi';
import type { Course } from '../types/course';



function CoursesPage() {

    const [courses, setCourses] = useState<Course[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {

        async function loadCourses() {

            try {
                const data = await getCourses();
                setCourses(data);

                } catch {

                    setErrorMessage('Could not load courses');

                    } finally {
                        setIsLoading(false);

                        }

            }

        loadCourses();


        }, [])



    return (

        <section>
            <div className='flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between'>
                <div>
                    <p className='text-sm font-medium text-blue-600'>Courses</p>
                    <h1 className='mt-2 text-2xl font-semibold text-slate-900'>Course catalog</h1>
                    <p className='mt-2 text-slate-600'>Explore available courses and continue learning.</p>
                </div>
            </div>

            {isLoading && (
                <div className='mt-8 rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>Loading courses...</div>

                )}

            {errorMessage && (
                <div className='mt-8 rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                    {errorMessage}
                </div>
                )}

            {!isLoading && !errorMessage && courses.length === 0 && (
                <div className='mt-8 rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm'>
                    <h2 className='text-lg font-semibold text-slate-900'>
                        No courses yet
                    </h2>
                    <p className='mt-2 text-sm text-slate-600'>
                        Published courses will appear here.
                    </p>
                </div>

                )}

            {!isLoading && !errorMessage && courses.length > 0 && (
                <div className='mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-3'>
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
                            <h2 className='mt-4 text-lg font-semibold text-slate-950'>{course.title}</h2>
                            <p className='mt-2 line-clamp-3 text-sm text-slate-600'>{course.description || 'No description provided.'}</p>
                            <div className='mt-5 text-sm font-medium text-blue-600'>Open course</div>
                        </Link>

                        ))}

                </div>

                )}
        </section>
        );
    }

export default CoursesPage;