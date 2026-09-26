import { apiClient } from './client';
import type { QuizQuestion, QuizQuestionCreate } from '../types/quiz';

import type {
    AIQuizGenerationRequest,
    AIQuizGenerationResult,
    QuizQuestion,
    QuizQuestionCreate,
    } from '../types/quiz';


export async function getQuizQuestions(quizId: number): Promise<QuizQuestion[]> {

    const response = await apiClient.get<QuizQuestion[]>(`/quizzes/${quizId}/questions`,);

    return response.data;

    }

export async function createQuizQuestion(quizId: number, data: QuizQuestionCreate): Promise<QuizQuestion> {

    const response = await apiClient.post<QuizQuestion>(`/quizzes/${quizId}/questions`, data);

    return response.data;

    }

export async function generateQuizQuestions(
    quizId: number,
    data: AIQuizGenerationRequest,
    ): Promise<AIQuizGenerationResult> {
        const response = await apiClient.post<AIQuizGenerationResult>(
            `/quizzes/${quizId}/generate-questions`,
            data,
            );

        return response.data;
        }

