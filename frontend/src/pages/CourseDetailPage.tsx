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

import Button from '../components/ui/Button';
import { useAuth } from '../auth/AuthContext';
import { getCourseProgress } from '../api/coursesApi';
import { enrollInCourse, getMyEnrollments} from '../api/enrollmentsApi';
import { completeLesson, getMyProgress } from '../api/lessonsApi';
import type { CourseProgress } from '../types/course';
import type { Enrollment } from '../types/enrollment';
import type { LessonProgress } from '../types/lesson';

import { type FormEvent } from 'react';
import FormCard from '../components/ui/FormCard';
import { createLesson } from '../api/lessonsApi';
import { createQuiz } from '../api/quizzesApi';
import { createAssignment } from '../api/assignmentsApi';




function CourseDetailPage() {

    const { courseId } = useParams();

    const { user } = useAuth();
    // states

    // general
    const [course, setCourse] = useState<Course | null>(null);
    const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
    const [lessonProgress, setLessonProgress] = useState<LessonProgress[]>([]);
    const [courseProgress, setCourseProgress] = useState<CourseProgress | null>(null);
    const [actionError, setActionError] = useState('');
    const [lessons, setLessons] = useState<Lesson[]>([]);
    const [quizzes, setQuizzes] = useState<Quiz[]>([]);
    const [assignments, setAssignments] = useState<Assignment[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    // form states

    // lesson params
    const [lessonTitle, setLessonTitle] = useState('');
    const [lessonContent, setLessonContent] = useState('');

    // quiz params
    const [quizTitle, setQuizTitle] = useState('');
    const [quizDescription, setQuizDescription] = useState('');
     // assignment params
    const [assignmentTitle, setAssignmentTitle] = useState('');
    const [assignmentDescription, setAssignmentDescription] = useState('');
    const [assignmentDueAt, setAssignmentDueAt] = useState('');

    const [teacherActionError, setTeacherActionError] = useState('');

    // useful constants and helpers
    const isStudent = user?.role === 'student';
    const isEnrolled = enrollments.some(
            (enrollment) => enrollment.course_id === course?.id
        );

    const completedLessonIds = new Set(
            lessonProgress.map((progress) => progress.lesson_id),
        );

    const canManageCourse = user?.role === 'teacher' || user?.role === 'admin';

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

                if (isStudent) {

                    const [enrollmentData, lessonProgressData, courseProgressData] = await Promise.all([getMyEnrollments(), getMyProgress(), getCourseProgress(id)]);

                    setEnrollments(enrollmentData);
                    setLessonProgress(lessonProgressData);
                    setCourseProgress(courseProgressData);

                    }




                } catch {

                    setErrorMessage(`Could not load course content.`);


                    } finally {

                        setIsLoading(false);

                        }
            }

        loadCourseData();
        }, [courseId, user?.role]);


    async function handleCreateLesson(event: FormEvent<HTMLFormElement>) {

           event.preventDefault();

           if (!course) {
               return;
               }

           setTeacherActionError('');

           try {

               const lesson = await createLesson(course.id, {
                    title: lessonTitle.trim(),
                    content: lessonContent.trim() || null,
                   })

               setLessons((current) => [...current, lesson]);
               setLessonTitle('');
               setLessonContent('');

               } catch {
                   setTeacherActionError('Could not create lesson.');
                   }

        }

    async function handleCreateQuiz(event: FormEvent<HTMLFormElement>) {

        event.preventDefault();

        if (!course) {

            return;

            }

        setTeacherActionError('');

        try {
             const quiz = await createQuiz(course.id, {
                    title: quizTitle.trim(),
                    description: quizDescription.trim() || null,
                 });

             setQuizzes((current) => [...current, quiz]);
             setQuizTitle('');
             setQuizDescription('');

            } catch {
                setTeacherActionError('Could not create quiz.');
                }

        }


    async function handleCreateAssignment(event: FormEvent<HTMLFormElement>) {

        event.preventDefault();

        if (!course) {
                return;
            }

        setTeacherActionError('');

        try {

            const assignment = await createAssignment(course.id, {
                    title: assignmentTitle.trim(),
                    description: assignmentDescription.trim() || null,
                    due_at: assignmentDueAt ? new Date(assignmentDueAt).toISOString() : null,
                });

            setAssignments((current) => [...current, assignment]);
            setAssignmentTitle('');
            setAssignmentDescription('');
            setAssignmentDueAt('');

            } catch {
                setTeacherActionError('Could not create assignment.');
                }
        }





    async function handleEnroll() {

        if (!course) {
                return;

            }

        setActionError('');

        try {
            const enrollment = await enrollInCourse(course.id);
            setEnrollments((current) => [enrollment, ...current]);

            const progress = await getCourseProgress(course.id);
            setCourseProgress(progress);

            } catch {

                setActionError('Could not enroll in this course.');

                }

        }

    async function handleCompleteLesson(lessonId: number) {

        if (!course) {
                return;
            }

        setActionError('');
        try {

            const progress = await completeLesson(lessonId);
            setLessonProgress((current) => [progress, ...current]);

            const updatedCourseProgress = await getCourseProgress(course.id);
            setCourseProgress(updatedCourseProgress);

            } catch {

                setActionError('Could not mark this lesson complete');

                }
        }


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
            <Link className='text-sm text-blue-600 hover:text-blue-700' to='/courses'>
                Back to courses
            </Link>

            <div className='mt-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'>
                    <span className='rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium capitalize text-blue-700'>
                        {course.status}
                    </span>

                    <h1 className='mt-4 text-2xl font-semibold text-slate-950'>
                        {course.title}
                    </h1>

                    <p className='mt-3 max-w-3xl text-slate-600'>
                        {course.description || 'No description provided.'}
                    </p>

                    {isStudent && (
                            <div className='mt-5 border-t border-slate-100 pt-5'>
                                {isEnrolled ? (
                                        <div>
                                            <p className='text-sm font-medium text-slate-900'>
                                                Progress: {courseProgress?.completed_lessons ?? 0}/
                                                {courseProgress?.total_lessons ?? lessons.length} lessons
                                            </p>

                                            <div className='mt-2 h-2 rounded-full bg-slate-100'>
                                                <div
                                                    className='h-2 rounded-full bg-blue-600'
                                                    style={{
                                                            width: `${courseProgress?.progress_percentage ?? 0}%`,
                                                        }}
                                                />
                                            </div>
                                        </div>

                                    ) : (
                                            <Button type='button' onClick={handleEnroll}>
                                                Enroll in course
                                            </Button>

                                        )}

                                    {actionError && (
                                            <p className='mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                                                {actionError}
                                            </p>
                                        )}
                            </div>
                        )}
            </div>

            {canManageCourse && (
                    <div className='mt-6'>
                        {teacherActionError && (
                            <p className='mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                                {teacherActionError}
                            </p>
                            )}

                        <div className='grid gap-4 lg:grid-cols-3'>
                            <FormCard title='Add lesson'>
                                <form className='space-y-3' onSubmit={handleCreateLesson}>
                                    <input
                                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Lesson title'
                                        value={lessonTitle}
                                        onChange={(event) => setLessonTitle(event.target.value)}
                                        required
                                     />

                                     <textarea
                                        className='min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Lesson content'
                                        value={lessonContent}
                                        onChange={(event) => setLessonContent(event.target.value)}
                                      />

                                      <Button type='submit'>Create lesson</Button>
                                </form>
                            </FormCard>

                            <FormCard title='Add quiz'>
                                <form className='space-y-3' onSubmit={handleCreateQuiz}>
                                    <input
                                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Quiz title'
                                        value={quizTitle}
                                        onChange={(event) => setQuizTitle(event.target.value)}
                                        required
                                    />

                                    <textarea
                                        className='min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Quiz description'
                                        value={quizDescription}
                                        onChange={(event) => setQuizDescription(event.target.value)}
                                     />

                                     <Button type='submit'>Create quiz</Button>

                                </form>
                            </FormCard>

                            <FormCard title='Add assignment'>
                                <form className='space-y-3' onSubmit={handleCreateAssignment}>
                                    <input
                                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Assignment title'
                                        value={assignmentTitle}
                                        onChange={(event) => setAssignmentTitle(event.target.value)}
                                        required
                                     />

                                     <textarea
                                        className='min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        placeholder='Assignment description'
                                        value={assignmentDescription}
                                        onChange={(event) => setAssignmentDescription(event.target.value)}
                                      />

                                     <input
                                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                                        type='datetime-local'
                                        value={assignmentDueAt}
                                        onChange={(event) => setAssignmentDueAt(event.target.value)}

                                      />

                                     <Button type='submit'>Create assignment</Button>
                                </form>
                            </FormCard>
                        </div>
                    </div>
                )}

            <div className='mt-6 grid gap-4 lg:grid-cols-3'>
                <ContentPanel title='Lessons' emptyText='No lessons yet.'>
                    {lessons.map((lesson) => {
                        const isCompleted = completedLessonIds.has(lesson.id);

                        return (
                            <div
                                key={lesson.id}
                                className='border-b border-slate-100 py-3 last:border-0'
                            >
                                <div className='flex items-start justify-between gap-3'>
                                    <div>
                                        <h3 className='font-medium text-slate-900'>{lesson.title}</h3>
                                        <p className='mt-1 text-sm text-slate-600'>
                                            {lesson.content || 'No content provided.'}
                                        </p>
                                    </div>

                                    {isStudent && isEnrolled && (
                                        isCompleted ? (
                                                <span className='rounded-md bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700'>
                                                    Completed
                                                </span>
                                            ) : (
                                                    <Button
                                                        className='shrink-0 px-3 py-1.5'
                                                        type='button'
                                                        variant='secondary'
                                                        onClick={() => handleCompleteLesson(lesson.id)}
                                                    >
                                                        Complete
                                                    </Button>
                                                )
                                        )}

                                </div>
                            </div>

                            );

                        })}
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