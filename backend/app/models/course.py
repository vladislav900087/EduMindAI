from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base



class CourseStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

class Currency(str, Enum):
    KZT = 'KZT'
    EUR = 'EUR'


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    currency: Mapped[Currency] = mapped_column(String(3), nullable=False, default=Currency.KZT, server_default=Currency.KZT.value)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[CourseStatus] = mapped_column(String(20), nullable=False, default=CourseStatus.DRAFT, server_default=CourseStatus.DRAFT.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    teacher = relationship('User')