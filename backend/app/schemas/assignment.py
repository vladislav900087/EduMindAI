from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class AssignmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_at: datetime | None = None


class AssignmentRead(BaseModel):
    id: int
    title: str
    description: str | None
    course_id: int
    due_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

