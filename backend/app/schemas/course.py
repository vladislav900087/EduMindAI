from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.course import CourseStatus, Currency


class CourseCreate(BaseModel):
    title:  str = Field(min_length=1, max_length=200)
    description: str | None = None
    price_amount: int = Field(default=0, ge=0, le=100_000_000)
    currency: Currency = Currency.KZT



class CourseRead(BaseModel):
    id: int
    title: str
    description: str | None
    teacher_id: int
    status: CourseStatus
    price_amount: int
    currency: Currency
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    