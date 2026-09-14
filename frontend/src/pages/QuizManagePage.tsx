import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import { getQuizQuestions, createQuizQuestion } from '../api/quizQuestionsApi';
import QuizQuestionForm from '../components/quizzes/QuizQuestionForm';
import FormCard from '../components/ui/FormCard';
import type { QuizQuestion, QuizQuestionCreate } from '../types/quiz';


function QuizManagePage() {

    const { quizId } = useParams();

    const [questions, setQuestions] = useState<QuizQuestion[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        async function loadQuestions() {
            if (!quizId) {
                setErrorMessage('Quiz id is missing.');
                setIsLoading(false);
                return;

                }

            try {
                const data = await getQuizQuestions(Number(quizId));
                setQuestions(data);
                } catch {
                    setErrorMessage('Could not load quiz questions.');
                    } finally {
                        setIsLoading(false);
                        }
            }

        loadQuestions();
        }, [quizId])

    async function handleCreateQuestion(data: QuizQuestionCreate) {
        if (!quizId) {
            return;
            }

        const question = await createQuizQuestion(Number(quizId), data);
        setQuestions((current) => [...current, question]);


        }

    return (
        <section>
            <Link className='text-sm font-medium text-blue-600 hover:text-blue-700' to='/courses'>
                Back to courses
            </Link>

            <div className='mt-5'>
                <p className='text-sm font-medium text-blue-600'>Quiz management</p>
                <h1 className='mt-2 text-2xl font-semibold text-slate-900'>
                    Quiz #{quizId} questions
                </h1>

            </div>

            <div className='mt-6 grid gap-6 lg:grid-cols-[420px_1fr]'>
                <FormCard title='Add question'>
                    <QuizQuestionForm onSubmit={handleCreateQuestion}/>
                </FormCard>

                <section className='rounded-lg border border-slate-200 bg-white p-5 shadow-sm'>
                    <h2 className='text-lg font-semibold text-slate-900'>Questions</h2>

                    {isLoading && (
                        <p className='mt-4 text-sm text-slate-600'>Loading questions...</p>
                        )}

                    {errorMessage && (
                        <p className='mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                            {errorMessage}
                        </p>
                        )}

                    {!isLoading && !errorMessage && questions.length === 0 && (
                        <p className='mt-4 text-sm text-slate-600'>
                            No questions added yet.
                        </p>
                        )}

                    {!isLoading && !errorMessage && questions.length > 0 && (
                        <div className='mt-4 space-y-4'>
                            {questions.map((question, questionIndex) => (
                                <article
                                    key={question.id}
                                    className='rounded-lg border border-slate-200 p-4'
                                >
                                    <h3 className='font-medium text-slate-900'>
                                        {questionIndex + 1}. {question.question_text}
                                    </h3>

                                    <div className='mt-3 space-y-2'>
                                        {question.options.map((option) => (
                                            <div
                                                key={option.id}
                                                className={[
                                                    'rounded-md border px-3 py-2 text-sm',
                                                    option.is_correct
                                                        ? 'border-green-200 bg-green-50 text-green-700'
                                                        : 'border-slate-200 text-slate-600',

                                                    ].join(' ')}
                                            >
                                            {option.option_text}
                                            {option.is_correct && (
                                                <span className='ml-2 text-xs font-medium'>
                                                    Correct
                                                </span>
                                                )}
                                            </div>
                                            ))}
                                    </div>
                                </article>
                                ))}
                        </div>
                        )}
                </section>

            </div>
        </section>
        );
    }

export default QuizManagePage;