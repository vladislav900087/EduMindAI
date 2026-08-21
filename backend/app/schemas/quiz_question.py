from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class QuizOptionCreate(BaseModel):
    option_text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False

class QuizQuestionCreate(BaseModel):
    question_text: str = Field(min_length=1)
    options: list[QuizOptionCreate] = Field(min_length=1)

class QuizOptionRead(BaseModel):
    id: int
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)

class QuizQuestionRead(BaseModel):
    id: int
    question_text: str
    quiz_id: int
    created_at: datetime
    options: list[QuizOptionRead]

    model_config = ConfigDict(from_attributes=True)

