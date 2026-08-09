from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.course import Course

class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, course: Course) -> Course:
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)

        return course

    def get_by_id(self, course_id: int) -> Course | None:
        statement = select(Course).where(Course.id == course_id)

        return self.db.scalar(statement)

    def list_all(self) -> list[Course]:
        statement = select(Course).order_by(Course.created_at.desc())

        return list(self.db.scalars(statement))

    def list_by_teacher(self, teacher_id: int) -> list[Course]:
        statement = select(Course).where(Course.teacher_id == teacher_id).order_by(Course.created_at.desc())

        return list(self.db.scalars(statement))