from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Integer, String

from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.database import Base

class UserRole(str, Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

class UserRegion(str, Enum):
    KAZAKHSTAN = 'kazakhstan'
    EUROPE = 'europe'


class InterfaceLanguage(str, Enum):
    ENGLISH = 'en'
    RUSSIAN = 'ru'
    KAZAKH = 'kk'
    GERMAN = 'de'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    region: Mapped[str] = mapped_column(String(20), nullable=False, default=UserRegion.KAZAKHSTAN.value, server_default=UserRegion.KAZAKHSTAN.value)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default=InterfaceLanguage.ENGLISH.value, server_default=InterfaceLanguage.ENGLISH.value)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))





