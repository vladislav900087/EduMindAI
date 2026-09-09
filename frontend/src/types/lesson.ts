
export type Lesson = {
    id: number;
    title: string;
    content: string | null;
    course_id: number;
    created_at: string;

    };

export type LessonProgress = {
    id: number;
    student_id: number;
    lesson_id: number;
    completed_at: string;

    };

export type LessonCreateRequest = {

    title: string;
    content?: string | null;

    };