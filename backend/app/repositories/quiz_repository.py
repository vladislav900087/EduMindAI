from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.quiz import Quiz

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, quiz: Quiz) -> Quiz:
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)

        return quiz

    def get_by_id(self, quiz_id: int) -> Quiz:
        statement = select(Quiz).where(Quiz.id == quiz_id)

        return self.db.scalar(statement)

    def list_by_course(self, course_id: int) -> list[Quiz]:
        statement = select(Quiz).where(Quiz.course_id == course_id)

        return list(self.db.scalars(statement))

