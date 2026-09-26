
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

export type QuizTakingOption = {
    id: number;
    option_text: string;

    };

export type QuizTakingQuestion = {
    id: number;
    question_text: string;
    options: QuizTakingOption[];
    };


export type QuizAttempt = {
    id: number;
    student_id: number;
    quiz_id: number;
    score: number | null;
    started_at: string;
    completed_at: string | null;
    };

export type QuizAttemptStart = {
    attempt: QuizAttempt;
    questions: QuizTakingQuestion[];
    };

export type QuizAnswerSubmit = {
    question_id: number;
    selected_option_id: number;
    };

export type QuizAnswer = {
    id: number;
    attempt_id: number;
    question_id: number;
    selected_option_id: number;
    };

export type AIQuizDifficulty = 'easy' | 'medium' | 'hard';

export type AIQuizGenerationRequest = {
    source_text: string;
    question_count: number;
    difficulty: AIQuizDifficulty;
    };

export type AIQuizGenerationResult = {
    questions: QuizQuestionCreate[];
    };



