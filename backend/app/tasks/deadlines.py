from backend.app.core.celery_app import celery_app
from backend.app.db.session import SessionLocal
from backend.app.repositories.assignment_deadline_reminder_repository import AssignmentDeadlineReminderRepository
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.assignment_deadline_reminder_service import AssignmentDeadlineReminderService
from backend.app.services.email_service import email_service
from backend.app.services.notification_service import NotificationService








@celery_app.task(bind=True, max_retries=3)
def send_assignment_deadline_reminders(self) -> str:
    db = SessionLocal()

    try:
        notification_service = NotificationService(email_service=email_service)
        service = AssignmentDeadlineReminderService(assignment_repository=AssignmentRepository(db=db), submission_repository=AssignmentSubmissionRepository(db=db), enrollment_repository=CourseEnrollmentRepository(db), notification_service=notification_service, reminder_repository=AssignmentDeadlineReminderRepository(db=db))

        sent_count = service.send_24_hour_reminders()

        return f'Sent {sent_count} assignment deadline reminder(s).'

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

    finally:
        db.close()





