from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.course import CourseStatus

class CourseCreate(BaseModel):
    title:  str = Field(min_length=1, max_length=200)
    description: str | None = None


class CourseRead(BaseModel):
    id: int
    title: str
    description: str | None
    teacher_id: int
    status: CourseStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    