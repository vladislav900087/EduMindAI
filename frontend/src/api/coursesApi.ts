import { apiClient } from './client';
import type { Course, CourseCreateRequest, CourseProgress } from '../types/course';

export async function getCourses(): Promise<Course[]> {

    const response = await apiClient.get<Course[]>('/courses');

    return response.data;

    }

export async function getMyCourses(): Promise<Course[]> {

    const response = await apiClient.get<Course[]>('/courses/my');

    return response.data;

    }

export async function getCourse(courseId: number): Promise<Course> {

    const response = await apiClient.get<Course>(`/courses/${courseId}`);

    return response.data;

    }

export async function createCourse(data: CourseCreateRequest): Promise<Course> {

    const response = await apiClient.post<Course>('/courses', data);

    return response.data;

    }

export async function publishCourse(courseId: number): Promise<Course> {

    const response = await apiClient.post<Course>(`/courses/${courseId}/publish`);

    return response.data;

    }

export async function getCourseProgress(courseId: number): Promise<CourseProgress> {

    const response = await apiClient.get<CourseProgress>(`/courses/${courseId}/progress`);

    return response.data;

    }