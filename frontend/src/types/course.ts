export type CourseStatus = 'draft' | 'published' | 'archived';


export type Course = {

    id: number;
    title: string;
    description: string | null;
    teacher_id: number;
    status: CourseStatus;
    created_at: string;

    };

export type CourseCreateRequest = {

    title: string;
    description?: string | null;


    };

export type CourseProgress = {
    course_id: number;
    total_lessons: number;
    completed_lessons: number;
    progress_percentage: number;

    };