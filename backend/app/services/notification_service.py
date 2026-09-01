from backend.app.services.email_service import EmailService
from datetime import datetime




class NotificationService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    def notify_assignment_graded(self, student_email: str, assignment_title: str, grade: int, feedback: str | None = None):

        message = f'Your assignment {assignment_title} is {grade}!'
        if feedback is not None:
            message = message + f'\n Feedback: {feedback}'

        self.email_service.send_email(recipient=str(student_email), subject='Assignment Graded', message_content=message)

    def notify_assignment_deadline(self, student_email: str, assignment_title: str, due_at: datetime) -> None:
        message = (
            f'Reminder: your assignment {assignment_title} is soon.\n'
            f'Deadline: {due_at}.'
        )

        self.email_service.send_email(recipient=student_email, subject='Assignment Deadline Reminder', message_content=message)











