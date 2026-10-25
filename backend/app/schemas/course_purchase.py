from pydantic import BaseModel, ConfigDict
from datetime import datetime
from backend.app.models.course_purchase import Currency, PurchaseStatus


class CoursePurchaseRead(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    course_id: int
    price_amount: int
    currency: Currency
    status: PurchaseStatus
    purchased_at: datetime

    model_config = ConfigDict(from_attributes=True)


