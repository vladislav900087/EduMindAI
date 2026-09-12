import { apiClient } from './client';
import type { Enrollment } from '../types/enrollment';


export async function getMyEnrollments(): Promise<Enrollment[]> {

    const response = await apiClient.get<Enrollment[]>('/enrollments/me');

    return response.data;

    }

export async function enrollInCourse(courseId: number): Promise<Enrollment> {

    const response = await apiClient.post<Enrollment>(`/enrollments/courses/${courseId}/enroll`,);

    return response.data;

    }

export async function unenrollFromCourse(courseId: number): Promise<void> {

    await apiClient.delete(`/enrollments/courses/${courseId}/unenroll`);


    }