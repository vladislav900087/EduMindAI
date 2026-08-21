from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class QuizQuestion(Base):

    __tablename__ = 'quiz_questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizzes.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    quiz = relationship('Quiz')
    options = relationship('QuizOption', back_populates='question')

