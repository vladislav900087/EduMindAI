from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.quiz_attempt_answer import QuizAttemptAnswer


class QuizAttemptAnswerRepository:
    def __init__(self, db: Session):

        self.db = db

    def create(self, answer: QuizAttemptAnswer) -> QuizAttemptAnswer:

        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)

        return answer

    def get_by_id(self, answer_id: int) -> QuizAttemptAnswer:
        statement = (select(QuizAttemptAnswer).where(QuizAttemptAnswer.id == answer_id))

        return self.db.scalar(statement)

    def get_by_attempt_and_question(self, attempt_id: int, question_id: int) -> QuizAttemptAnswer | None:
        statement = (select(QuizAttemptAnswer).where(QuizAttemptAnswer.attempt_id == attempt_id, QuizAttemptAnswer.question_id == question_id))

        return self.db.scalar(statement)

    def list_by_attempt(self, attempt_id: int) -> list[QuizAttemptAnswer]:

        statement = (select(QuizAttemptAnswer).where(QuizAttemptAnswer.attempt_id == attempt_id).order_by(QuizAttemptAnswer.id.asc()))

        return list(self.db.scalars(statement))

