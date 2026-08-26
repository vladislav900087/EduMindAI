from pydantic import BaseModel

class QuizAttemptCreate(BaseModel):
    question_id: int
    selected_option_id: int

class QuizAnswerRead(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    selected_option_id: int

