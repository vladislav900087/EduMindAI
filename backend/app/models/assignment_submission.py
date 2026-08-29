from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Text, func, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped

from backend.app.db.database import Base

class AssignmentSubmission(Base):
    __tablename__ = 'assignment_submissions'

    __table_args__ = (UniqueConstraint('student_id', 'assignment_id', name='uq_assignment_submission_student_assignment'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey('assignments.id'), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    grade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    graded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student = relationship('User')
    assignment = relationship('Assignment')
