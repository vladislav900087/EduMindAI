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

            setIsGenerating(true);
            setErrorMessage('');
            setDrafts([]);


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
                                                ...option
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

        }
    }



