from backend.app.core.celery_app import celery_app
from backend.app.services.notification_service import NotificationService
from backend.app.services.email_service import email_service




@celery_app.task(bind=True, max_retries=3)
def send_assignment_graded_notification(self, student_email: str, assignment_title: str, grade: int, feedback: str | None = None):
    try:
        service = NotificationService(email_service=email_service)
        service.notify_assignment_graded(student_email=student_email, assignment_title=assignment_title, grade=grade, feedback=feedback)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
