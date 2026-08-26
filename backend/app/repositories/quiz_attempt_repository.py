from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.quiz_attempt import QuizAttempt

class QuizAttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, attempt: QuizAttempt) -> QuizAttempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)

        return attempt

    def get_by_id(self, attempt_id: int) -> QuizAttempt | None:
        statement = (select(QuizAttempt).where(QuizAttempt.id == attempt_id))

        return self.db.scalar(statement)

    def list_by_student(self, student_id: int) -> list[QuizAttempt]:
        statement = (select(QuizAttempt).where(QuizAttempt.student_id == student_id).order_by(QuizAttempt.started_at.desc()))

        return list(self.db.scalars(statement))

    def list_by_quiz(self, quiz_id: int) -> list[QuizAttempt]:

        statement = (select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id).order_by(QuizAttempt.started_at.desc()))

        return list(self.db.scalars(statement))

    def update(self, attempt: QuizAttempt) -> QuizAttempt:
        self.db.commit()
        self.db.refresh(attempt)

        return attempt