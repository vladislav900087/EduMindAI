from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from backend.app.db.database import Base

class QuizAttemptAnswer(Base):

    __tablename__ = 'quiz_attempt_answers'

    __table_args__ = (UniqueConstraint('attempt_id', 'question_id', name='uq_quiz_attempt_question'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey('quiz_attempts.id'), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey('quiz_questions.id'), nullable=False)
    selected_option_id: Mapped[int] = mapped_column(ForeignKey('quiz_options.id'), nullable=False)

    attempt = relationship('QuizAttempt')
    question = relationship('QuizQuestion')
    selected_option = relationship('QuizOption')


