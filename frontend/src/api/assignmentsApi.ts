import { apiClient } from './client';
import type { Assignment, AssignmentCreateRequest, AssignmentSubmission, AssignmentSubmitRequest } from '../types/assignment';


export async function getCourseAssignments(courseId: number): Promise<Assignment[]> {

    const response = await apiClient.get<Assignment[]>(`/assignments/courses/${courseId}`);

    return response.data;

    }

export async function createAssignment(courseId: number, data: AssignmentCreateRequest): Promise<Assignment> {

    const response = await apiClient.post<Assignment>(`/assignments/courses/${courseId}`, data);

    return response.data;

    }

export async function getAssignment(assignmentId: number): Promise<Assignment> {

    const response = await apiClient.get<Assignment>(`assignments/${assignmentId}`);

    return response.data;
    }

export async function getMySubmissions(): Promise<AssignmentSubmission[]> {

    const response = await apiClient.get<AssignmentSubmission[]>('/submissions/me');

    return response.data;

    }

export async function submitAssignment(assignmentId: number, data: AssignmentSubmitRequest): Promise<AssignmentSubmission> {

    const response = await apiClient.post<AssignmentSubmission>(`/assignments/${assignmentId}/submissions`, data);

    return response.data;
    }


export async function updateAssignmentSubmission(submissionId: number, data: AssignmentSubmitRequest): Promise<AssignmentSubmission> {

    const response = await apiClient.put<AssignmentSubmission>(`/submissions/${submissionId}`, data);

    return response.data;

    }