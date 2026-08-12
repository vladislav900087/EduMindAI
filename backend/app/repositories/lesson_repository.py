from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.lesson import Lesson

class LessonRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, lesson: Lesson) -> Lesson:
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)

        return lesson

    def get_by_id(self, lesson_id: int) -> Lesson:
        statement = select(Lesson).where(Lesson.id == lesson_id)

        return self.db.scalar(statement)

    def list_by_course(self, course_id: int) -> list[Lesson]:
        statement = select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.created_at.asc())

        return list(self.db.scalars(statement))

    def delete(self, lesson: Lesson) -> None:
        self.db.delete(lesson)
        self.db.commit()
