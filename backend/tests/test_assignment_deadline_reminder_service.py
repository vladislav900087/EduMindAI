from datetime import timedelta, timezone, datetime

from backend.app.models.assignment import Assignment
from backend.app.models.assignment_submission import AssignmentSubmission
from backend.app.models.course import Course
from backend.app.models.course_enrollment import CourseEnrollment
from backend.app.models.user import User, UserRole

from backend.app.repositories.assignment_deadline_reminder_repository import AssignmentDeadlineReminderRepository
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.assignment_deadline_reminder_service import AssignmentDeadlineReminderService
from backend.app.services.notification_service import NotificationService
from backend.app.services.email_service import email_service


class FakeNotificationService:
    def __init__(self):
        self.sent = []

    def notify_assignment_deadline(self, student_email, assignment_title, due_at):
        self.sent.append({
            'student_email': student_email,
            'assignment_title': assignment_title,
            'due_at': due_at
        })


def create_teacher(db_session):
    teacher = User(email='deadline-teacher@example.com', hashed_password='hashed', full_name='Deadline Teacher', role=UserRole.TEACHER)

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    return teacher

def create_student(db_session, email='deadline-student@example.com'):
    student = User(email=email, hashed_password='hashed', full_name='Deadline Student', role=UserRole.STUDENT)

    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)

    return student

def create_course(db_session, teacher):
    course = Course(title='Deadline Course', description='Deadline Course Test Description', teacher_id=teacher.id)

    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    return course

def create_assignment(db_session, course, due_at):
    assignment = Assignment(title='Deadline Assignment', description='Deadline Assignment Test Description', course_id=course.id, due_at=due_at)

    db_session.add(assignment)
    db_session.commit()
    db_session.refresh(assignment)

    return assignment

def enroll_student(db_session, student, course):
    enrollment = CourseEnrollment(student_id=student.id, course_id=course.id)

    db_session.add(enrollment)
    db_session.commit()
    db_session.refresh(enrollment)

    return enrollment

def build_service(db_session, notification_service):
    return AssignmentDeadlineReminderService(assignment_repository=AssignmentRepository(db_session), enrollment_repository=CourseEnrollmentRepository(db_session), submission_repository=AssignmentSubmissionRepository(db_session), reminder_repository=AssignmentDeadlineReminderRepository(db_session), notification_service=notification_service)



def test_send_24_hour_reminders_sends_email_to_enrolled_student(db_session):
    student = create_student(db_session)
    teacher = create_teacher(db_session)
    course = create_course(db_session, teacher)

    due_at = datetime.now(timezone.utc) + timedelta(hours=12)
    assignment = create_assignment(db_session, course, due_at)

    enroll_student(db_session, student, course)

    notification_service = FakeNotificationService()
    service = build_service(db_session, notification_service)

    sent_count = service.send_24_hour_reminders()

    assert sent_count == 1
    assert len(notification_service.sent) == 1
    assert notification_service.sent[0]['student_email'] == student.email
    assert notification_service.sent[0]['assignment_title'] == assignment.title

def test_send_24_hour_reminders_skips_student_already_reminded(db_session):
    student = create_student(db_session)
    teacher = create_teacher(db_session)
    course = create_course(db_session, teacher)

    due_at = datetime.now(timezone.utc) + timedelta(hours=12)

    assignment = create_assignment(db_session, course, due_at)

    enroll_student(db_session, student, course)

    repository = AssignmentDeadlineReminderRepository(db_session)
    notification_service = FakeNotificationService()
    service = build_service(db_session, notification_service)

    repository.create(assignment_id=assignment.id, student_id=student.id, reminder_type=service.REMINDER_TYPE_24_HOURS)
    sent_count = service.send_24_hour_reminders()

    assert sent_count == 0
    assert notification_service.sent == []

def test_send_24_hour_reminders_skips_assignment_due_later(db_session):
    student = create_student(db_session)
    teacher = create_teacher(db_session)
    course = create_course(db_session, teacher)

    due_at = datetime.now(timezone.utc) + timedelta(days=3)

    assignment = create_assignment(db_session, course, due_at)

    enroll_student(db_session, student, course)

    notification_service = FakeNotificationService()

    service = build_service(db_session, notification_service)

    sent_count = service.send_24_hour_reminders()

    assert sent_count == 0
    assert notification_service.sent == []

def test_send_24_hour_reminders_records_sent_reminder(db_session):
    student = create_student(db_session)
    teacher = create_teacher(db_session)
    course = create_course(db_session, teacher)

    due_at = datetime.now(timezone.utc) + timedelta(hours=12)

    assignment = create_assignment(db_session, course, due_at)

    enroll_student(db_session, student, course)

    notification_service = FakeNotificationService()

    service = build_service(db_session, notification_service)

    service.send_24_hour_reminders()

    reminder_repository = AssignmentDeadlineReminderRepository(db_session)

    assert reminder_repository.exists(assignment_id=assignment.id, student_id=student.id, reminder_type=service.REMINDER_TYPE_24_HOURS) is True


def test_send_24_hour_reminders_actually_sends_gmail_message(db_session):
    student = create_student(db_session)
    teacher = create_teacher(db_session)
    course = create_course(db_session, teacher)

    due_at = datetime.now(timezone.utc) + timedelta(hours=12)

    assignment = create_assignment(db_session, course, due_at)

    enroll_student(db_session, student, course)

    notification_service = NotificationService(email_service)

    service = build_service(db_session, notification_service)

    service.send_24_hour_reminders()

    repository = AssignmentDeadlineReminderRepository(db_session)

    assert repository.exists(assignment_id=assignment.id, student_id=student.id, reminder_type=service.REMINDER_TYPE_24_HOURS) is True











































