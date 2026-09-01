from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

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

    def list_due_between(self, start_at: datetime, end_at: datetime) -> list[Assignment]:
        assignments = self.db.query(Assignment).filter(Assignment.due_at.isnot(None), Assignment.due_at >= start_at, Assignment.due_at <= end_at).all()
        return list(assignments)


    def update(self, assignment: Assignment) -> Assignment:
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def delete(self, assignment: Assignment) -> None:
        self.db.delete(assignment)
        self.db.commit()
