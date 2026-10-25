import type { Currency} from './payment';

export type CourseStatus = 'draft' | 'published' | 'archived';


export type Course = {

    id: number;
    title: string;
    description: string | null;
    teacher_id: number;
    status: CourseStatus;
    price_amount: number;
    currency: Currency;
    created_at: string;

    };

export type CourseCreateRequest = {

    title: string;
    description?: string | null;
    price_amount?: number | null;
    currency?: Currency | null;


    };

export type CourseProgress = {
    course_id: number;
    total_lessons: number;
    completed_lessons: number;
    progress_percentage: number;

    };