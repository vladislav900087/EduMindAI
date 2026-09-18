
export type Assignment = {

    id: number;
    title: string;
    description: string | null;
    course_id: number;
    due_at: string | null;
    created_at: string;

    };

export type AssignmentCreateRequest = {

    title: string;
    description?: string | null;
    due_at?: string | null;

    };

export type AssignmentSubmission = {

    id: number;
    assignment_id: number;
    student_id: number;
    content: string;
    submitted_at: string;
    updated_at: string | null;
    grade: number | null;
    feedback: string | null;
    graded_at: string | null;

    };

export type AssignmentSubmitRequest = {
    content: string;

    };

export type AssignmentGradeRequest = {

    grade: number;
    feedback?: string | null;
    }