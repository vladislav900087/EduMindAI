import { apiClient } from './client';
import type { Quiz, QuizCreateRequest } from '../types/quiz';


export async function getCourseQuizzes(courseId: number): Promise<Quiz[]> {

    const response = await apiClient.get<Quiz[]>(`/courses/${courseId}/quizzes`);

    return response.data;

    }


export async function createQuiz(courseId: number, data: QuizCreateRequest): Promise<Quiz> {

    const response = await apiClient.post<Quiz>(`/courses/${courseId}/quizzes`, data);

    return response.data;

    }