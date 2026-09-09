import { apiClient } from './client';
import type { Assignment, AssignmentCreateRequest } from '../types/assignment';


export async function getCourseAssignments(courseId: number): Promise<Assignment[]> {

    const response = await apiClient.get<Assignment[]>(`/assignments/courses/${courseId}`);

    return response.data;

    }

export async function createAssignment(courseId: number, data: AssignmentCreateRequest): Promise<Assignment> {

    const response = await apiClient.post<Assignment>(`/assignments/courses/${courseId}`, data);

    return response.data;

    }