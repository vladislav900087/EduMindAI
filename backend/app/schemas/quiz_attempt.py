from datetime import datetime

from pydantic import BaseModel, ConfigDict

class QuizAttemptRead(BaseModel):
    id: int
    student_id: int
    quiz_id: int
    score: float | None
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class QuizTakingOptionRead(BaseModel):
    id: int
    option_text: str


class QuizTakingQuestionRead(BaseModel):
    id: int
    question_text: str
    options: list[QuizTakingOptionRead]


class QuizAttemptStartRead(BaseModel):
    attempt: QuizAttemptRead
    questions: list[QuizTakingQuestionRead]


class QuizAnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int

class QuizAnswerRead(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    selected_option_id: int
