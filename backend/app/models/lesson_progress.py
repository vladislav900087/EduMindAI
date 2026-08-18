from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class LessonProgress(Base):

    __tablename__ = 'lesson_progress'

    __table_args__ = (UniqueConstraint('student_id', 'lesson_id', name='uq_lesson_progress_student_lesson'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id'), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship('User')
    lesson = relationship('Lesson')