
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


export type QuizOptionCreate = {
    option_text: string;
    is_correct: boolean;

    };

export type QuizQuestionCreate = {
    question_text: string;
    options: QuizOptionCreate[];

    };

export type QuizOption = {
    id: number;
    option_text: string;
    is_correct: boolean;
    };

export type QuizQuestion = {
    id: number;
    question_text: string;
    quiz_id: number;
    created_at: string;
    options: QuizOption[];

    };