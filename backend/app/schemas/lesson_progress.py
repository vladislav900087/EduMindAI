from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonProgressRead(BaseModel):
    id: int
    student_id: int
    lesson_id: int
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseProgressRead(BaseModel):
    course_id: int
    total_lessons: int
    completed_lessons: int
    progress_percentage: float



