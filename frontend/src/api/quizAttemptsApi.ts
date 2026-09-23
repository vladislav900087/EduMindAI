import { apiClient } from './client';
import type { QuizAnswer, QuizAnswerSubmit, QuizAttempt, QuizAttemptStart} from '../types/quiz';


export async function startQuizAttempt(quizId: number): Promise<QuizAttemptStart> {
    const response = await apiClient.post<QuizAttemptStart>(`/quizzes/${quizId}/attempts`,);

    return response.data;


    }

export async function submitQuizAnswer(attemptId: number, data: QuizAnswerSubmit): Promise<QuizAnswer> {

    const response = await apiClient.post<QuizAnswer>(`/attempts/${attemptId}/answers`, data);

    return response.data;


    }

export async function completeQuizAttempt(attemptId: number): Promise<QuizAttempt> {
    const response = await apiClient.post<QuizAttempt>(`/attempts/${attemptId}/complete`,);

    return response.data;
    }

export async function getMyCompletedQuizAttempts(): Promise<QuizAttempt[]> {

    const response = await apiClient.get<QuizAttempt[]>('/attempts/me');
    return response.data;

    }

