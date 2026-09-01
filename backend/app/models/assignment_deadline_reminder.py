from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from backend.app.db.database import Base


class AssignmentDeadlineReminder(Base):
    __tablename__ = 'assignment_deadline_reminders'

    __table_args__ = (UniqueConstraint('assignment_id', 'student_id', 'reminder_type', name='uq_assignment_deadline_reminder_assignment_student_type',),)

    id: Mapped[int] = mapped_column(primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey('assignments.id'), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    reminder_type: Mapped[str] = mapped_column(String(50), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    assignment = relationship('Assignment')
    student = relationship('User')








