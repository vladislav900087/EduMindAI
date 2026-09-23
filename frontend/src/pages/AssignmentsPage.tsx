import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { getCourseAssignments, getMySubmissions } from '../api/assignmentsApi';
import { getMyCourses, getCourses } from '../api/coursesApi';
import { getMyEnrollments } from '../api/enrollmentsApi';
import { useAuth } from '../auth/AuthContext';
import type { Assignment, AssignmentSubmission } from '../types/assignment';
import type { Course } from '../types/course';


type AssignmentRow = {
    assignment: Assignment;
    course: Course;
    submission?: AssignmentSubmission;
    };

function AssignmentsPage() {

    const { user } = useAuth();
    const isStudent = user?.role === 'student';

    const [rows, setRows] = useState<AssignmentRow[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');


    useEffect(() => {
        async function loadAssignments() {

            setIsLoading(true);
            setErrorMessage('');

            try {
                    let courses: Course[];

                    if (isStudent) {
                            const [enrollments, catalog] = await Promise.all([getMyEnrollments(), getCourses(),]);
                            const enrolledIds = new Set(enrollments.map((enrollment) => enrollment.course_id),
                            );
                            courses = catalog.filter((course) => enrolledIds.has(course.id),);
                        } else {
                            courses = await getMyCourses();
                            }

                        const [assignmentsByCourse, submissions] = await Promise.all([
                            Promise.all(
                                courses.map((course) => getCourseAssignments(course.id),
                                ),
                            ),

                            isStudent
                                ? getMySubmissions()
                                : Promise.resolve([] as AssignmentSubmission[]),
                            ]);

                        const submissionByAssignment = new Map(
                            submissions.map((submission) => [submission.assignment_id, submission]),
                            );

                        const allRows = courses.flatMap((course, index) => assignmentsByCourse[index].map((assignment) => (
                            {
                                assignment,
                                course,
                                submission: submissionByAssignment.get(assignment.id),
                                })),
                            );

                        allRows.sort((a, b) => {
                            if (!a.assignment.due_at) return 1;
                            if (!b.assignment.due_at) return -1;

                            return (
                                new Date(a.assignment.due_at).getTime() - new Date(b.assignment.due_at).getTime()
                                );
                            });

                        setRows(allRows);
                } catch {
                    setErrorMessage('Could not load assignments');

                    } finally {
                        setIsLoading(false);
                        }


            }

        loadAssignments();
        }, [isStudent]);

    function getStatus(row: AssignmentRow): string {

        if (!isStudent) return row.course.status;

        if (row.submission?.grade !== null && row.submission?.grade !== undefined) {
            return `Graded: ${row.submission.grade}/100`;
            }

        if (row.submission) return 'Submitted';

        if (row.assignment.due_at && new Date(row.assignment.due_at).getTime() < Date.now()) {

            return 'Closed';

            }

        return 'To do';

        }


    return (
        <section>
            <h1 className='text-2xl font-semibold text-slate-950'>
                Assignments
            </h1>

            {isLoading && (
                <p className='mt-5 text-sm text-slate-600'>
                    Loading assignments...
                </p>
                )}

            {errorMessage && (
                <p className='mt-5 rounded-md bg-red-50 p-4 text-sm text-red-700'>
                    {errorMessage}
                </p>
                )}

            {!isLoading && !errorMessage && rows.length == 0 && (
                <p className='mt-5 text-sm text-slate-600'>
                    No assignments yet.
                </p>
                )}

            {!isLoading && !errorMessage && rows.length > 0 && (
                <div className='mt-5 overflow-hidden rounded-lg border border-slate-200 bg-white'>
                    {rows.map((row) => (
                        <Link
                            key={row.assignment.id}
                            to={`/assignments/${row.assignment.id}`}
                            className='flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 p-4 last:border-b-0 hover:bg-slate-50'
                        >
                            <div className='min-w-0'>
                                <h2 className='font-medium text-slate-900'>
                                    {row.assignment.title}
                                </h2>
                                <p className='mt-1 text-sm text-slate-500'>
                                    {row.course.title}
                                    {' · Due: '}
                                    {row.assignment.due_at ? new Date(row.assignment.due_at).toLocaleString() : 'No deadline'}

                                </p>
                            </div>
                            <span className='text-sm font-medium text-slate-700'>
                                {getStatus(row)}
                            </span>
                        </Link>

                        ))}
                </div>
                )}
        </section>

        );

    }

export default AssignmentsPage;