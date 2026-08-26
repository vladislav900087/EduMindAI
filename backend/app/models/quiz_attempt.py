from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class QuizAttempt(Base):

    __tablename__ = 'quiz_attempts'

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quizzes.id'), nullable=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student = relationship('User')
    quiz = relationship('Quiz')