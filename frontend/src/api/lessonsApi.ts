import { apiClient } from './client';
import type { Lesson, LessonCreateRequest, LessonProgress } from '../types/lesson';

export async function getCourseLessons(courseId: number): Promise<Lesson[]> {

    const response = await apiClient.get<Lesson[]>(`/courses/${courseId}/lessons`);

    return response.data;

    }

export async function createLesson(courseId: number, data: LessonCreateRequest): Promise<Lesson> {

    const response = await apiClient.post<Lesson>(`/courses/${courseId}/lessons`, data);
    return response.data;

    }

export async function completeLesson(lessonId: number): Promise<LessonProgress> {

    const response = await apiClient.post<LessonProgress>(`/lessons/${lessonId}/complete`);
    return response.data;

    }

export async function getMyProgress(): Promise<LessonProgress[]> {

    const response = await apiClient.get<LessonProgress[]>('/lessons/progress/me');
    return response.data;

    }