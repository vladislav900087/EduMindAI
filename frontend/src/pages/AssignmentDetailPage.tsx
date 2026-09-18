import { useParams, Link } from 'react-router-dom';
import { useEffect, useState, type FormEvent } from 'react';
import {
    getAssignment,
    getMySubmissions,
    submitAssignment,
    updateAssignmentSubmission
    } from '../api/assignmentsApi';

import { useAuth } from '../auth/AuthContext';
import Button from '../components/ui/Button';
import type { Assignment, AssignmentSubmission } from '../types/assignment';


function AssignmentDetailPage() {

    const { assignmentId } = useParams();
    const { user } = useAuth();

    const [assignment, setAssignment] = useState<Assignment | null>(null);
    const [submission, setSubmission] = useState<AssignmentSubmission | null>(null);
    const [content, setContent] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const isStudent = user?.role === 'student';


    useEffect(() => {

        async function loadAssignment() {

            if (!assignmentId) {
                setErrorMessage('Assignment id is missing');
                setIsLoading(false);
                return;
                }

            try
                {
                    const assignmentData = await getAssignment(Number(assignmentId));
                    setAssignment(assignmentData);

                    if (isStudent) {
                        const submissions = await getMySubmissions();
                        const existingSubmission = submissions.find(
                            (item) => item.assignment_id === Number(assignmentId),
                            );

                        if (existingSubmission) {
                            setSubmission(existingSubmission);
                            setContent(existingSubmission.content);
                            }
                        }

                    } catch {
                        setErrorMessage('Could not load the assignment.');
                        } finally {
                            setIsLoading(false);
                            }



            }

        loadAssignment();

        }, [assignmentId, isStudent]);

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {

        event.preventDefault();

        if (!assignment || !content.trim()) {
            setErrorMessage('Submission content is required.');
            return;

            }

        setIsSaving(true);
        setErrorMessage('');
        setSuccessMessage('');

        try {
            const savedSubmission = submission ? await updateAssignmentSubmission(submission.id, {content: content.trim()}) : await submitAssignment(assignment.id, {content: content.trim()});

            setSubmission(savedSubmission);
            setContent(savedSubmission.content);
            setSuccessMessage(submission ? 'Submission updated successfully.' : 'Assignment submitted successfully.');

            } catch {
                setErrorMessage('Could not save the submission');
                } finally {
                    setIsSaving(false);
                    }
        }

    if (isLoading) {
        return <p className='text-sm text-slate-600'>Loading assignment...</p>;
        }

    if (!assignment) {
        return (
            <div className='rounded-md bg-red-50 p-4 text-sm text-red-700'>
                {errorMessage || 'Assignment was not found.'}
            </div>
            );
        }

    const isGraded = submission?.grade !== null && submission?.grade !== undefined;



    return (
        <section>
            <Link
                to={`/courses/${assignment.course_id}`}
                className='text-sm font-medium text-blue-600 hover:text-blue-700'
            >
                Back to course
            </Link>

            <div className='mt-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'>
                <p className='text-sm font-medium text-blue-600'>
                    Assignment
                </p>

                <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
                    {assignment.title}
                </h1>

                <p className='mt-3 whitespace-pre-wrap text-slate-600'>
                    {assignment.description || 'No description provided.'}
                </p>

                <p className='mt-4 text-sm text-slate-500'>
                    Due:{' '}
                    {assignment.due_at ? new Date(assignment.due_at).toLocaleString() : 'No deadline'}
                </p>
            </div>

            {isStudent && (
                    <form
                        onSubmit={handleSubmit}
                        className='mt-6 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'
                    >
                        <h2 className='text-lg font-semibold text-slate-900'>
                            Your submission
                        </h2>

                        <textarea
                            value={content}
                            disabled={isGraded}
                            maxLength={1000}
                            rows={8}
                            onChange={(event) => setContent(event.target.value)}
                            className='mt-4 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:bg-slate-100'
                            placeholder="Write your answer..."
                         />

                         <p className='mt-1 text-right text-xs text-slate-500'>
                            {content.length}/1000
                         </p>

                         {errorMessage && (
                             <p className='mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                                {errorMessage}
                             </p>
                             )}

                         {successMessage && (
                             <p className='mt-3 rounded-md bg-green-50 px-3 py-2 text-sm text-green-700'>
                                {successMessage}
                             </p>
                             )}

                         {isGraded && submission && (
                             <div className='mt-4 rounded-md bg-blue-50 p-4'>
                                <p className='font-semibold text-blue-900'>
                                    Grade: {submission.grade}
                                </p>
                                <p className='mt-1 text-sm text-blue-800'>
                                    {submission.feedback || 'No feedback provided.'}
                                </p>
                             </div>
                             )}

                         {!isGraded && (
                             <div className='mt-4'>
                                <Button
                                    type='submit'
                                    disabled={isSaving || !content.trim()}
                                >
                                    {isSaving
                                        ? 'Saving...'
                                        : submission
                                          ? 'Update submission'
                                          : 'Submit assignment'

                                        }
                                </Button>
                             </div>
                             )}
                    </form>
                )}

        </section>

        );


    }

export default AssignmentDetailPage;


