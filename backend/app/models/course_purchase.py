from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from backend.app.db.database import Base
from backend.app.models.course import Currency


class PurchaseStatus(str, Enum):
    COMPLETED = 'completed'
    REFUNDED = 'refunded'


class CoursePurchase(Base):

    __tablename__ = 'course_purchases'

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_course_purchase_student_course',
                         ),
        CheckConstraint('price_amount > 0', name='ck_course_purchase_price_amount_positive')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[Currency] = mapped_column(String(3), nullable=False)
    status: Mapped[PurchaseStatus] = mapped_column(String(20), nullable=False, default=PurchaseStatus.COMPLETED, server_default=PurchaseStatus.COMPLETED)
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    student = relationship('User', foreign_keys=[student_id])
    teacher = relationship('User', foreign_keys=[teacher_id])
    course = relationship('Course')