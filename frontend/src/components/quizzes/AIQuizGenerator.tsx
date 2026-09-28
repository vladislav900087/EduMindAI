import { useState, type FormEvent } from 'react';

import {
    createQuizQuestion,
    generateQuizQuestions,
    } from '../../api/quizQuestionsApi';

import type {
    AIQuizDifficulty,
    QuizQuestion,
    QuizQuestionCreate,
    } from '../../types/quiz';

import Button from '../ui/Button';

type Props = {
    quizId: number;
    onQuestionSaved: (question: QuizQuestion) => void;
    };

function AIQuizGenerator({ quizId, onQuestionSaved }: Props) {

        const [sourceText, setSourceText] = useState('');
        const [questionCount, setQuestionCount] = useState(5);
        const [difficulty, setDifficulty] = useState<AIQuizDifficulty>('medium');
        const [drafts, setDrafts] = useState<QuizQuestionCreate[]>([]);
        const [isGenerating, setIsGenerating] = useState(false);
        const [savingIndex, setSavingIndex] = useState<number | null>(null);
        const [errorMessage, setErrorMessage] = useState('');

        async function handleGenerate(event: FormEvent<HTMLFormElement>) {

            event.preventDefault();

            if (sourceText.trim().length < 20) {
                setErrorMessage(
                    'Provide at least 20 characters of source material.'
                    );
                return;
                }

            if (
                !Number.isInteger(questionCount) ||
                questionCount < 1 ||
                questionCount > 10
                ) {
                    setErrorMessage('Question count must be between 1 and 10.');
                    return;
                    }

            setIsGenerating(true);
            setErrorMessage('');



            try {
                    const result = await generateQuizQuestions(quizId, {
                        source_text: sourceText.trim(),
                        question_count: questionCount,
                        difficulty,
                        });

                    setDrafts(result.questions);
                } catch {
                    setErrorMessage(
                        'Could not generate questions. Check the AI configuration and try again.',
                        );
                    } finally {
                            setIsGenerating(false);
                        }
            }

        function updateQuestion(index: number, questionText: string) {

            setDrafts((current) =>
                current.map((question, questionIndex) =>
                    questionIndex === index
                        ? { ...question, question_text: questionText }
                        : question,
                ),
            );
        }

    function updateOption(
        questionIndex: number,
        optionIndex: number,
        optionText: string,
        ) {
            setDrafts((current) =>
                current.map((question, currentQuestionIndex) =>
                    currentQuestionIndex === questionIndex
                        ? {
                                ...question,
                                options: question.options.map(
                                    (option, currentOptionIndex) =>
                                        currentOptionIndex === optionIndex
                                            ? {
                                                ...option,
                                                option_text: optionText,
                                                }
                                            : option,
                                 ),
                            }
                        : question,
                ),
            );
        }

    function selectCorrectOption(
        questionIndex: number,
        correctOptionIndex: number,
        ) {

            setDrafts((current) =>
                current.map((question, currentQuestionIndex) =>
                    currentQuestionIndex === questionIndex
                        ? {
                            ...question,
                            options: question.options.map(
                                (option, optionIndex) => ({
                                        ...option,
                                        is_correct:
                                            optionIndex === correctOptionIndex,
                                    }),
                                ),
                            }
                        : question,
                ),
            );
        }

    function discardQuestion(index: number) {
            setDrafts((current) =>
                current.filter((_, questionIndex) => questionIndex !== index),
            );
        }

    async function saveQuestion(index: number) {
        const draft = drafts[index]

        if (!draft.question_text.trim() ||
            draft.options.some((option) => !option.option_text.trim())) {
                setErrorMessage(
                    'Question text and all four options are required.'
                    );
                return;
                }

        if (draft.options.filter((option) => option.is_correct).length !== 1) {

            setErrorMessage(
                'Each question must have exactly one correct option.'
                );
            return;

            }

        setSavingIndex(index);
        setErrorMessage('');

        try {

            const saved = await createQuizQuestion(quizId, {
                question_text: draft.question_text.trim(),
                options: draft.options.map((option) => ({
                        option_text: option.option_text.trim(),
                        is_correct: option.is_correct,
                    })),
                });

            onQuestionSaved(saved);
            discardQuestion(index);

            } catch {
                setErrorMessage('Could not save the generated question.');
                } finally {
                        setSavingIndex(null);
                    }

        }

    return (
        <section className='mt-6 border-y border-slate-200 bg-white py-6'>
            <h2 className='text-lg font-semibold text-slate-900'>
                Generate with AI
            </h2>

            <form onSubmit={handleGenerate} className='mt-4 space-y-4'>
                <label className='block'>
                    <span className='text-sm font-medium text-slate-700'>
                        Source material
                    </span>

                    <textarea
                        rows={8}
                        minLength={20}
                        maxLength={12000}
                        required
                        value={sourceText}
                        onChange={(event) =>
                            setSourceText(event.target.value)
                            }
                        placeholder='Paste lesson notes or educational material...'
                        className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
                     />
                     <span className='mt-1 block text-right text-xs text-slate-500'>
                        {sourceText.length}/12000
                     </span>
                </label>

                <div className='flex flex-wrap gap-4'>
                    <label>
                        <span className='block text-sm font-medium text-slate-700'>
                            Questions
                        </span>
                        <input
                            type='number'
                            min={1}
                            max={10}
                            value={questionCount}
                            onChange={(event) => setQuestionCount(Number(event.target.value))}
                            className='mt-1 w-24 rounded-md border border-slate-300 px-3 py-2 text-sm'
                         />
                    </label>

                    <label>
                        <span className='block text-sm font-medium text-slate-700'>
                            Difficulty
                        </span>
                        <select
                            value={difficulty}
                            onChange={(event) => setDifficulty(event.target.value as AIQuizDifficulty)}
                            className='mt-1 rounded-md border border-slate-300 px-3 py-2 text-sm'
                        >
                            <option value='easy'>Easy</option>
                            <option value='medium'>Medium</option>
                            <option value='hard'>Hard</option>
                        </select>
                    </label>
                </div>

                <Button type='submit' disabled={isGenerating}>
                    {isGenerating ? 'Generating...' : 'Generate preview'}
                </Button>
            </form>

            {errorMessage && (
                <p className='mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700'>
                    {errorMessage}
                </p>
                )}

            {drafts.length > 0 && (
                <div className='mt-8 space-y-5'>
                    <div>
                        <h3 className='font-semibold text-slate-900'>
                            Review generated questions
                        </h3>
                        <p className='mt-1 text-sm text-slate-600'>
                            Edit each draft and save only the questions you approve.
                        </p>
                    </div>

                    {drafts.map((question, questionIndex) => (
                        <article
                            key={questionIndex}
                            className='rounded-lg border border-slate-200 p-4'
                        >
                            <label className='block'>
                                <span className='text-sm font-medium text-slate-700'>
                                    Question {questionIndex + 1}
                                </span>

                                <textarea
                                    value={question.question_text}
                                    onChange={(event) => updateQuestion(questionIndex, event.target.value)}
                                    className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm'
                                 />
                            </label>

                            <div className='mt-4 space-y-2'>
                                {question.options.map((option, optionIndex) => (
                                    <div
                                        key={optionIndex}
                                        className='flex items-center gap-3'
                                    >
                                    <input
                                        type='radio'
                                        name={`ai-correct-${questionIndex}`}
                                        checked={option.is_correct}
                                        onChange={() => selectCorrectOption(
                                                questionIndex,
                                                optionIndex
                                            )}
                                     />

                                     <input
                                        value={option.option_text}
                                        onChange={(event) => updateOption(questionIndex, optionIndex, event.target.value)}
                                        className='w-full rounded-md border border-slate-300 px-3 py-2 text-sm'
                                      />
                                    </div>
                                    ))}
                            </div>

                            <div className='mt-4 flex gap-2'>
                                <Button
                                    type='button'
                                    disabled={savingIndex !== null}
                                    onClick={() =>
                                        saveQuestion(questionIndex)
                                        }
                                >
                                    {savingIndex === questionIndex ? 'Saving' : 'Approve and save'}
                                </Button>

                                <Button
                                    type='button'
                                    disabled={savingIndex !== null}
                                    variant='secondary'
                                    onClick={() => discardQuestion(questionIndex)}
                                >
                                    Discard
                                </Button>
                            </div>
                        </article>
                        ))}
                </div>
                )}
        </section>
        );
    }

export default AIQuizGenerator;



