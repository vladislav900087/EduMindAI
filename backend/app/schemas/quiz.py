from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class QuizCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class QuizRead(BaseModel):
    id: int
    title: str
    description: str | None
    course_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)