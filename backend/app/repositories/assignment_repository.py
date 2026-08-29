from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.assignment import Assignment

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, assignment: Assignment) -> Assignment:
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def get_by_id(self, assignment_id: int) -> Assignment:

        statement = (select(Assignment).where(Assignment.id == assignment_id))

        return self.db.scalar(statement)

    def list_by_course(self, course_id: int) -> list[Assignment]:
        statement = (select(Assignment).where(Assignment.course_id == course_id).order_by(Assignment.created_at.asc()))

        return list(self.db.scalars(statement))

    def update(self, assignment: Assignment) -> Assignment:
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def delete(self, assignment: Assignment) -> None:
        self.db.delete(assignment)
        self.db.commit()
