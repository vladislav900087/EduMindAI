import { useParams, Link } from 'react-router-dom';
import { useEffect, useState, useMemo} from 'react';

import { completeQuizAttempt, startQuizAttempt, submitQuizAnswer } from '../api/quizAttemptsApi';
import Button from '../components/ui/Button';
import type { QuizAttempt, QuizTakingQuestion } from '../types/quiz';



function QuizTakingPage() {

    const { quizId } = useParams();

    const [attempt, setAttempt] = useState<QuizAttempt | null>(null);
    const [questions, setQuestions] = useState<QuizTakingQuestion[]>([]);
    const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
    const [submittedQuestionIds, setSubmittedQuestionIds] = useState<number[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isCompleting, setIsCompleting] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        async function startAttempt() {
            if (!quizId) {
                setErrorMessage('Quiz id is missing.');
                setIsLoading(false);
                return;
                }

            try {
                const data = await startQuizAttempt(Number(quizId));
                setAttempt(data.attempt);
                setQuestions(data.questions);
                } catch {
                    setErrorMessage('Could not start quiz attempt.');
                    } finally {
                        setIsLoading(false);
                        }
            }
        startAttempt();
        }, [quizId]);

    const allQuestionsAnswered = useMemo(() => {
        return (
            questions.length > 0 && questions.every((question) => submittedQuestionIds.includes(question.id))
            );
        }, [questions, submittedQuestionIds]);

    async function handleSubmitAnswer(questionId: number) {
        if (!attempt) {
            return;
            }

        const selectedOptionId = selectedAnswers[questionId];

        if (!selectedOptionId) {
            setErrorMessage('Choose an answer before submitting.');
            return;
            }

        setErrorMessage('');

        try {
            await submitQuizAnswer(attempt.id, {
                question_id: questionId,
                selected_option_id: selectedOptionId,
                });

            setSubmittedQuestionIds((current) => [...current, questionId]);
            } catch {
                setErrorMessage('Could not submit answer.');
                }
        }

    async function handleCompleteAttempt() {
        if (!attempt) {
            return;
            }

        setIsCompleting(true);
        setErrorMessage('');

        try {

            const completedAttempt = await completeQuizAttempt(attempt.id);
            setAttempt(completedAttempt);

            } catch {
                setErrorMessage('Could not complete quiz.');
                } finally {
                    setIsCompleting(false);
                    }
        }

    if (isLoading) {
        return (
            <section className='rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600 shadow-sm'>
                Starting quiz...
            </section>
            );
        }

    if (errorMessage && !attempt) {
        return (
            <section className='rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                {errorMessage}
            </section>
            )
        }

    if (!attempt) {
        return (
            <section className='rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-700'>
                Quiz attempt was not created.
            </section>
            )
        }

    const isCompleted = attempt.completed_at !== null;


    return (
        <section>
            <Link className='text-sm font-medium text-blue-600 hover:text-blue-700' to='/courses'>
                Back to courses
            </Link>

            <div className='mt-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm'>
                <p className='text-sm font-medium text-blue-600'>
                    Quiz attempt
                </p>
                <h1 className='mt-2 text-2xl font-semibold text-slate-950'>
                    Quiz #{attempt.quiz_id}
                </h1>

                {isCompleted && (
                    <div className='mt-4 rounded-lg bg-green-50 p-4 text-green-700'>
                        Quiz completed. Score: {attempt.score ?? 0}%
                    </div>
                    )}
            </div>

            {errorMessage && (
                    <div className='mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                        {errorMessage}
                    </div>
                    )}

             <div className='mt-6 space-y-4'>
                {questions.map((question, index) => {
                        const isSubmitted = submittedQuestionIds.includes(question.id);

                        return (
                            <article
                                key={question.id}
                                className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'
                            >
                                <h2
                                    className='font-semibold text-slate-900'
                                >
                                    {index + 1}. {question.question_text}
                                </h2>

                                <div className='mt-4 space-y-2'>
                                    {question.options.map((option) => (
                                        <label
                                            key={option.id}
                                            className={[
                                                'flex cursor-pointer items-center gap-3 rounded-md border px-3 py-2 text-sm',
                                                selectedAnswers[question.id] === option.id
                                                    ? 'border-blue-300 bg-blue-50 text-blue-700'
                                                    : 'border-slate-200 text-slate-700',
                                                isSubmitted || isCompleted ? 'cursor-not-allowed opacity-70' : '',

                                                ].join(' ')}
                                        >
                                            <input
                                                type='radio'
                                                name={`question-${question.id}`}
                                                value={option.id}
                                                checked={selectedAnswers[question.id] === option.id}
                                                disabled={isSubmitted || isCompleted}
                                                onChange={() =>
                                                    setSelectedAnswers((current) => ({
                                                        ...current,
                                                        [question.id]: option.id
                                                        }))
                                                    }
                                             />
                                             {option.option_text}
                                        </label>
                                        ))}
                                </div>

                                {!isCompleted && (
                                    <div className='mt-4 '>
                                        {isSubmitted ? (
                                            <span className='rounded-md bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700'>
                                                Answer submitted
                                            </span>
                                            ) : (
                                                <Button
                                                    type='button'
                                                    variant='secondary'
                                                    onClick={() => handleSubmitAnswer(question.id)}
                                                 >
                                                    Submit answer
                                                 </Button>
                                                )
                                        }
                                    </div>
                                    )}
                            </article>
                            );
                    })}
             </div>

             {!isCompleted && (
                 <div className='mt-6 rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <Button
                        type='button'
                        disabled={!allQuestionsAnswered || isCompleting}
                        onClick={handleCompleteAttempt}
                    >
                        {isCompleting ? 'Completing...' : 'Complete quiz'}
                    </Button>

                    {!allQuestionsAnswered && (
                        <p className='mt-2 text-sm text-slate-600'>
                            Submit all answers before completing the quiz.
                        </p>
                        )}
                 </div>
                 )}
        </section>
        );
    }

export default QuizTakingPage;