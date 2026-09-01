from backend.app.models.assignment_deadline_reminder import AssignmentDeadlineReminder
from sqlalchemy.orm import Session

class AssignmentDeadlineReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, assignment_id: int, student_id: int, reminder_type: str) -> AssignmentDeadlineReminder:
        reminder = AssignmentDeadlineReminder(assignment_id=assignment_id, student_id=student_id, reminder_type=reminder_type)
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)

        return reminder

    def get_by_assignment_student_and_type(self, assignment_id: int, student_id: int, reminder_type: str) -> AssignmentDeadlineReminder | None:

        return (self.db.query(AssignmentDeadlineReminder).filter(AssignmentDeadlineReminder.assignment_id == assignment_id, AssignmentDeadlineReminder.student_id == student_id, AssignmentDeadlineReminder.reminder_type == reminder_type).first())

    def exists(self, assignment_id: int, student_id: int, reminder_type: str) -> bool:
        reminder = self.get_by_assignment_student_and_type(assignment_id=assignment_id, student_id=student_id, reminder_type=reminder_type)

        return reminder is not None



