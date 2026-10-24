from backend.app.models.course_purchase import CoursePurchase
from sqlalchemy import select
from sqlalchemy.orm import Session


class CoursePurchaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_purchase(self, student_id: int, course_id: int) -> CoursePurchase | None:

        statement = select(CoursePurchase).where(CoursePurchase.student_id == student_id, CoursePurchase.course_id == course_id)

        return self.db.scalar(statement)

    def create_without_commit(self, course_purchase: CoursePurchase) -> CoursePurchase:

        self.db.add(course_purchase)
        self.db.flush()

        return course_purchase

    def create(self, course_purchase: CoursePurchase) -> CoursePurchase:

        self.db.add(course_purchase)
        self.db.commit()
        self.db.refresh(course_purchase)

        return course_purchase