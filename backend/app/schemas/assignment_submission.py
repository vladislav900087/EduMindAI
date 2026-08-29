from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class AssignmentSubmissionCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class AssignmentSubmissionRead(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    content: str
    submitted_at: datetime
    updated_at: datetime | None
    grade: int | None
    feedback: str | None
    graded_at: datetime | None


class AssignmentSubmissionGrade(BaseModel):
    grade: int
    feedback: str | None = None

