

from sqlalchemy import Boolean, String, ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from backend.app.db.database import Base

class QuizOption(Base):

    __tablename__ = 'quiz_options'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('quiz_questions.id'), nullable=False)
    option_text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    question = relationship('QuizQuestion', back_populates='options')