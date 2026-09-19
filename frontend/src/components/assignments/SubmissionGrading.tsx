
import { useState, type FormEvent } from 'react';

import { gradeAssignmentSubmission } from '../../api/assignmentsApi';
import type { AssignmentSubmission } from '../../types/assignment';
import Button from '../ui/Button';

type Props = {
    submission: AssignmentSubmission;
    onGraded: (updated: AssignmentSubmission) => void;
    }

function SubmissionGrading({submission, onGraded}: Props) {

    const [grade, setGrade] = useState('');
    const [feedback, setFeedback] = useState('');
    const [isSaving, setIsSaving] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    async function handleGrade(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const numericGrade = Number(grade);

        if (!Number.isInteger(numericGrade) || numericGrade < 0 || numericGrade > 100) {
            setErrorMessage('Enter a whole-number grade from 0 to 100.');
            return;
            }

        setIsSaving(true);
        setErrorMessage('');

        try {
            const updated = await gradeAssignmentSubmission(submission.id, {
                grade: numericGrade,
                feedback: feedback.trim() || null,
                });

            onGraded(updated);
            } catch {
                setErrorMessage('Could not grade this submission');
                } finally {
                    setIsSaving(false);
                    }

        }

    return (
        <article className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
            <div className='flex flex-wrap items-start justify-between gap-3'>
                <div>
                    <h3 className='font-semibold text-slate-900'>
                        Student #{submission.student_id}
                    </h3>
                    <p className='mt-1 text-xs text-slate-500'>
                        Submitted {new Date(submission.submitted_at).toLocaleString()}
                    </p>
                </div>
                {submission.grade !== null && (
                    <span className='rounded-md bg-green-50 px-3 py-1 text-sm font-medium text-green-700'>
                        {submission.grade}/100
                    </span>
                    )}
            </div>
            <p className='mt-4 whitespace-pre-wrap text-sm text-slate-700'>
                {submission.content}
            </p>

            {submission.grade !== null ? (
                <p className='mt-4 text-sm text-slate-600'>
                    Feedback: {submission.feedback || 'No feedback provided.'}
                </p>
                ) : (
                    <form onSubmit={handleGrade} className='mt-5 space-y-3'>
                        <div>
                            <label
                                htmlFor={`grade-${submission.id}`}
                                className='block text-sm font-medium text-slate-700'
                            >
                                Grade
                            </label>
                            <input
                                id={`grade-${submission.id}`}
                                type='number'
                                min={0}
                                max={100}
                                step={1}
                                required
                                value={grade}
                                onChange={(event) => setGrade(event.target.value)}
                                className='mt-1 w-24 rounded-md border border-slate-300 px-3 py-2 text-sm'
                             />
                        </div>

                        <div>
                            <label
                                htmlFor={`feedback-${submission.id}`}
                                className='block text-sm font-medium text-slate-700'
                            >
                                Feedback
                            </label>
                            <textarea
                                id={`feedback-${submission.id}`}
                                rows={3}
                                value={feedback}
                                onChange={(event) => setFeedback(event.target.value)}
                                className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm'
                             />
                        </div>
                        {errorMessage && (
                            <p className='text-sm text-red-700'>
                                {errorMessage}
                            </p>
                            )}

                        <Button
                            type='submit'
                            disabled={isSaving}
                        >
                            {isSaving ? 'Saving...' : 'Save grade'}
                        </Button>
                    </form>
                    )}
        </article>


        );
    }

export default SubmissionGrading;