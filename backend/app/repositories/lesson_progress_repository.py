from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.lesson_progress import LessonProgress


class LessonProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_student_and_lesson(self, student_id: int, lesson_id: int) -> LessonProgress | None:
        return self.db.scalar(select(LessonProgress).where(LessonProgress.student_id == student_id, LessonProgress.lesson_id == lesson_id))

    def create(self, progress: LessonProgress) -> LessonProgress:
        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)

        return progress

    def list_by_student(self, student_id: int) -> list[LessonProgress]:
        return list(self.db.scalars(select(LessonProgress).where(LessonProgress.student_id == student_id).order_by(LessonProgress.completed_at)).all())

    def list_by_student_and_course(self, student_id: int, course_id: int) -> list[LessonProgress]:
        statement = select(LessonProgress).join(LessonProgress.lesson).where(LessonProgress.student_id == student_id, LessonProgress.lesson.has(course_id=course_id)).order_by(LessonProgress.completed_at)

        return list(self.db.scalars(statement).all())
