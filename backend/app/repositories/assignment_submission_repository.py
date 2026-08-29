from backend.app.models.assignment_submission import AssignmentSubmission
from sqlalchemy.orm import Session
from sqlalchemy import select


class AssignmentSubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, assignment_submission: AssignmentSubmission) -> AssignmentSubmission:
        self.db.add(assignment_submission)
        self.db.commit()
        self.db.refresh(assignment_submission)

        return assignment_submission

    def get_by_id(self, assignment_submission_id: int) -> AssignmentSubmission:
        statement = (select(AssignmentSubmission).where(AssignmentSubmission.id == assignment_submission_id))

        return self.db.scalar(statement)

    def get_by_student_and_assignment(self, student_id: int, assignment_id: int) -> AssignmentSubmission:
        statement = (select(AssignmentSubmission).where(AssignmentSubmission.student_id == student_id, AssignmentSubmission.assignment_id == assignment_id))

        return self.db.scalar(statement)


    def list_by_student(self, student_id: int) -> list[AssignmentSubmission]:
        statement = (select(AssignmentSubmission).where(AssignmentSubmission.student_id == student_id).order_by(AssignmentSubmission.submitted_at.desc()))

        return list(self.db.scalars(statement))

    def list_by_assignment(self, assignment_id: int) -> list[AssignmentSubmission]:

        statement = (select(AssignmentSubmission).where(AssignmentSubmission.assignment_id == assignment_id).order_by(AssignmentSubmission.submitted_at.desc()))

        return list(self.db.scalars(statement))

    def update(self, assignment_submission: AssignmentSubmission) -> AssignmentSubmission:
        self.db.commit()
        self.db.refresh(assignment_submission)

        return assignment_submission
