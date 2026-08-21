from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption



class QuizQuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_question(self, quiz_question: QuizQuestion) -> QuizQuestion:
        self.db.add(quiz_question)
        self.db.commit()
        self.db.refresh(quiz_question)

        return quiz_question

    def create_option(self, option: QuizOption) -> QuizOption:
        self.db.add(option)
        self.db.commit()
        self.db.refresh(option)

        return option

    def get_by_id(self, question_id: int) -> QuizQuestion:
        statement = (select(QuizQuestion).where(QuizQuestion.id == question_id))

        return self.db.scalar(statement)

    def list_by_quiz(self, quiz_id: int) -> list[QuizQuestion]:
        statement = (select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id).order_by(QuizQuestion.created_at.asc()))

        return list(self.db.scalars(statement))

    def list_options(self, question_id: int) -> list[QuizOption]:

        statement = (select(QuizOption).where(QuizOption.question_id == question_id).order_by(QuizOption.id.asc()))

        return list(self.db.scalars(statement))

    def delete(self, question: QuizQuestion) -> None:
        self.db.delete(question)
        self.db.commit()

