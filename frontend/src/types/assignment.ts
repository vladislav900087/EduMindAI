
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