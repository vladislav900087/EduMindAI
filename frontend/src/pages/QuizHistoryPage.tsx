import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { getMyCompletedQuizAttempts} from '../api/quizAttemptsApi';
import { getQuiz } from '../api/quizzesApi';
import type { Quiz, QuizAttempt } from '../types/quiz';


type HistoryRow = {
    attempt: QuizAttempt;
    quiz: Quiz;
    };

function QuizHistoryPage() {

    const [rows, setRows] = useState<HistoryRow[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {

        async function loadHistory() {

            try {
                const attempts = await getMyCompletedQuizAttempts();
                const quizIds = [...new Set(
                        attempts.map((attempt) => attempt.quiz_id),
                    )];

                const quizzes = await Promise.all(quizIds.map((quizId) => getQuiz(quizId)),
                );

                const quizzesById = new Map(
                    quizzes.map((quiz) => [quiz.id, quiz]),
                    );

                const historyRows = attempts.flatMap((attempt) => {
                    const quiz = quizzesById.get(attempt.quiz_id);
                    return quiz ? [{attempt, quiz}] : [];
                    });

                setRows(historyRows);



                } catch {
                    setErrorMessage('Could not load quiz history');
                    } finally {
                        setIsLoading(false);
                        }
            }

        loadHistory();

        }, []);

    return (
        <section>
            <h1 className='text-2xl font-semibold text-slate-950'>
                Quiz history
            </h1>
            <p className='mt-2 text-sm text-slate-600'>
                Your completed quiz attempts and scores.
            </p>

            {isLoading && (
                <p className='mt-5 text-sm text-slate-600'>
                    Loading quiz history...
                </p>
                )}

            {errorMessage && (
                <p className='mt-5 rounded-md bg-red-50 p-4 text-sm text-red-700'>
                    {errorMessage}
                </p>
                )}

            {!isLoading && !errorMessage && rows.length === 0 && (
                <p className='mt-5 text-sm text-slate-600'>
                    No completed quizzes yet.
                </p>
                )}

            {!isLoading && !errorMessage && rows.length > 0 && (
                <div className='mt-5 overflow-hidden rounded-lg border border-slate-200 bg-white'>
                    {rows.map(({ attempt, quiz }) => (
                        <div
                            key={attempt.id}
                            className='flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 p-4 last:border-b-0'
                        >
                            <div>
                                <Link
                                    to={`/courses/${quiz.course_id}`}
                                    className='font-medium text-slate-900 hover:text-blue-700'
                                >
                                    {quiz.title}
                                </Link>

                                <p className='mt-1 text-sm text-slate-500'>
                                    Completed{' '}
                                    {attempt.completed_at
                                        ? new Date(
                                            attempt.completed_at,
                                            ).toLocaleString()
                                        : ''}

                                </p>
                            </div>

                            <span className='text-lg font-semibold text-blue-700'>
                                {Math.round(attempt.score ?? 0)}%
                            </span>
                        </div>
                        ))}

                </div>
                )}
        </section>
        );


    }

export default QuizHistoryPage;