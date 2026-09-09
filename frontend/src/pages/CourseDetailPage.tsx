import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

import { getCourse } from '../api/coursesApi';
import { getCourseAssignments } from '../api/assignmentsApi';
import { getCourseLessons } from '../api/lessonsApi';
import { getCourseQuizzes } from '../api/quizzesApi';
import type { Course } from '../types/course';
import type { Assignment } from '../types/assignment';
import type { Lesson } from '../types/lesson';
import type { Quiz } from '../types/quiz';


function CourseDetailPage() {

    const { courseId } = useParams();

    const [course, setCourse] = useState<Course | null>(null);
    const [lessons, setLessons] = useState<Lesson[]>([]);
    const [quizzes, setQuizzes] = useState<Quiz[]>([]);
    const [assignments, setAssignments] = useState<Assignment[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {

        async function loadCourseData() {

            if (!courseId) {

                setErrorMessage('Course id is missing.');
                setIsLoading(false);
                return;


                }

            const id = Number(courseId);

            try {

                const [courseData, lessonData, quizData, assignmentData] = await Promise.all([getCourse(id), getCourseLessons(id), getCourseQuizzes(id), getCourseAssignments(id)]);

                setCourse(courseData);
                setLessons(lessonData);
                setQuizzes(quizData);
                setAssignments(assignmentData);


                } catch {

                    setErrorMessage('Could not load course content.');


                    } finally {

                        setIsLoading(false);

                        }
            }

        loadCourseData();
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
                    <span className='rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium capitalize text-blue-700'>
                        {course.status}
                    </span>

                    <h1 className='mt-4 text-2xl font-semibold text-slate-950'>
                        {course.title}
                    </h1>

                    <p className='mt-3 max-w-3xl text-slate-600'>
                        {course.description || 'No description provided.'}
                    </p>
                </div>
            </div>

            <div className='mt-6 grid gap-4 lg:grid-cols-3'>
                <ContentPanel title='Lessons' emptyText='No lessons yet.'>
                    {lessons.map((lesson) => (
                            <div key={lesson.id} className='border-b border-slate-100 py-3 last:border-0'>
                                <h3 className='font-medium text-slate-900'>{lesson.title}</h3>
                                <p className='mt-1 text-sm text-slate-600'>
                                    {lesson.content || 'No content provided.'}
                                </p>
                            </div>
                        ))}
                </ContentPanel>
                <ContentPanel title='Quizzes' emptyText='No quizzes yet.'>
                    {quizzes.map((quiz) => (
                            <Link
                                key={quiz.id}
                                className='block border-b border-slate-100 py-3 last:border-0'
                                to={`/quizzes/${quiz.id}/take`}
                            >
                                <h3 className='font-medium text-slate-900'>{quiz.title}</h3>
                                <p className='mt-1 text-sm text-slate-600'>
                                    {quiz.description || 'No description provided.'}
                                </p>
                            </Link>
                        ))}
                </ContentPanel>

                <ContentPanel title='Assignments' emptyText='No assignments yet.'>
                    {assignments.map((assignment) => (
                            <Link
                                key={assignment.id}
                                className='block border-b border-slate-100 py-3 last:border-0'
                                to={`/assignments/${assignment.id}`}
                            >
                                <h3 className='font-medium text-slate-900'>{assignment.title}</h3>
                                <p className='mt-1 text-sm text-slate-600'>
                                    {assignment.description || 'No description provided.'}
                                </p>

                                {assignment.due_at && (
                                        <p>
                                            Due: {new Date(assignment.due_at).toLocaleString()}
                                        </p>
                                    )}
                            </Link>


                        ))}
                </ContentPanel>
            </div>
        </section>
        );
    }

type ContentPanelProps = {

    title: string;
    emptyText: string;
    children: React.ReactNode[];

    };

function ContentPanel({ title, emptyText, children }: ContentPanelProps) {
        return (
                <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <h2 className='font-semibold text-slate-900'>{title}</h2>

                    <div className='mt-3'>
                        {children.length > 0 ? (
                                children
                            ) : (
                                    <p className='text-sm text-slate-600'>{emptyText}</p>

                                )}
                    </div>
                </section>

            );

    }

export default CourseDetailPage;