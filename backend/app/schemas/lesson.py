from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class LessonCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str | None = None

class LessonRead(BaseModel):
    id: int
    title: str
    content: str | None
    course_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)