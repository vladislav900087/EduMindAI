
export type Quiz = {
    id: number;
    title: string;
    description: string | null;
    course_id: number;
    created_at: string;

    };

export type QuizCreateRequest = {

    title: string;
    description?: string | null;

    };