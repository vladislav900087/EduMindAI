from datetime import datetime, timezone, timedelta
import logging

from backend.app.repositories.assignment_deadline_reminder_repository import AssignmentDeadlineReminderRepository
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.notification_service import NotificationService


logger = logging.getLogger(__name__)

class AssignmentDeadlineReminderService:
    REMINDER_TYPE_24_HOURS = '24_hours_before'

    def __init__(self, assignment_repository: AssignmentRepository, enrollment_repository: CourseEnrollmentRepository, submission_repository: AssignmentSubmissionRepository, reminder_repository: AssignmentDeadlineReminderRepository, notification_service: NotificationService):
        self.assignment_repository = assignment_repository
        self.enrollment_repository = enrollment_repository
        self.submission_repository = submission_repository
        self.reminder_repository = reminder_repository
        self.notification_service = notification_service

    def send_24_hour_reminders(self) -> int:
        now = datetime.now(timezone.utc)
        reminder_window_end = now + timedelta(hours=24)

        assignments = self.assignment_repository.list_due_between(start_at=now, end_at=reminder_window_end)

        set_count = 0

        for assignment in assignments:
            enrollments = self.enrollment_repository.list_by_course(assignment.course_id)

            for enrollment in enrollments:
                if self._student_already_submitted(student_id=enrollment.student_id, assignment_id=assignment.id):
                    continue

                if self._reminder_already_sent(student_id=enrollment.student_id, assignment_id=assignment.id, reminder_type=self.REMINDER_TYPE_24_HOURS):
                    continue

                student = enrollment.student

                try:
                    self.notification_service.notify_assignment_deadline(student_email=student.email, assignment_title=assignment.title, due_at=assignment.due_at)
                    self.reminder_repository.create(assignment_id=assignment.id, student_id=enrollment.student_id, reminder_type=self.REMINDER_TYPE_24_HOURS)

                    set_count += 1
                except Exception as exc:
                    logger.error('Failed to send assignment deadline reminder: %s', exc)

        return set_count

    def _student_already_submitted(self, student_id: int, assignment_id: int) -> bool:
        submission = self.submission_repository.get_by_student_and_assignment(student_id=student_id, assignment_id=assignment_id)

        return submission is not None

    def _reminder_already_sent(self, student_id: int, assignment_id: int, reminder_type: str) -> bool:
        return self.reminder_repository.exists(assignment_id=assignment_id, student_id=student_id, reminder_type=reminder_type)





































