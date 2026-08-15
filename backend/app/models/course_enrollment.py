from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class CourseEnrollment(Base):

    __tablename__ = 'course_enrollments'

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_course_enrollment_student_course'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship('User')
    course = relationship('Course')