import { apiClient } from './client';
import type { QuizQuestion, QuizQuestionCreate } from '../types/quiz';


export async function getQuizQuestions(quizId: number): Promise<QuizQuestion[]> {

    const response = await apiClient.get<QuizQuestion[]>(`/quizzes/${quizId}/questions`,);

    return response.data;

    }

export async function createQuizQuestion(quizId: number, data: QuizQuestionCreate): Promise<QuizQuestion> {

    const response = await apiClient.post<QuizQuestion>(`/quizzes/${quizId}/questions`, data);

    return response.data;

    }