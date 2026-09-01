import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.models.assignment import Assignment
from backend.app.models.assignment_deadline_reminder import AssignmentDeadlineReminder
from backend.app.models.course import Course
from backend.app.models.user import User, UserRole
from backend.app.repositories.assignment_deadline_reminder_repository import AssignmentDeadlineReminderRepository


def create_teacher(db_session):
    teacher = User(email='teacher@example.com', hashed_password='hashed', full_name='Teacher User', role=UserRole.TEACHER)

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    return teacher

def create_student(db_session):
    student = User(email='student@example.com', hashed_password='hashed', full_name='Student User', role=UserRole.STUDENT)

    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)

    return student

def create_assignment(db_session, teacher):
    course = Course(title='Python Basics', description='Intro Course', teacher_id=teacher.id)

    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    assignment = Assignment(title='Loops homework', description='Practice loops', course_id=course.id)

    db_session.add(assignment)
    db_session.commit()
    db_session.refresh(assignment)

    return assignment

def test_create_deadline_reminder(db_session):
    teacher = create_teacher(db_session)
    student = create_student(db_session)
    assignment = create_assignment(db_session, teacher)

    repository = AssignmentDeadlineReminderRepository(db_session)

    reminder = repository.create(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before')

    assert reminder.id is not None
    assert reminder.assignment_id == assignment.id
    assert reminder.student_id == student.id
    assert reminder.reminder_type == '24_hours_before'
    assert reminder.sent_at is not None

def test_get_by_assignment_student_and_type(db_session):

    teacher = create_teacher(db_session)
    student = create_student(db_session)
    assignment = create_assignment(db_session, teacher)

    repository = AssignmentDeadlineReminderRepository(db_session)

    created_reminder = repository.create(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before')

    assert created_reminder is not None

    found_reminder = repository.get_by_assignment_student_and_type(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before')

    assert found_reminder is not None
    assert found_reminder.id == created_reminder.id

def test_exists_returns_true_when_reminder_exists(db_session):
    teacher = create_teacher(db_session)
    student = create_student(db_session)
    assignment = create_assignment(db_session, teacher)

    repository = AssignmentDeadlineReminderRepository(db_session)

    repository.create(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before')

    assert repository.exists(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before') is True

def test_exists_returns_false_when_reminder_does_not_exist(db_session):
    teacher = create_teacher(db_session)
    student = create_student(db_session)
    assignment = create_assignment(db_session, teacher)

    repository = AssignmentDeadlineReminderRepository(db_session)

    assert repository.exists(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before') is False

def test_duplicate_reminder_is_not_allowed(db_session):
    teacher = create_teacher(db_session)
    student = create_student(db_session)
    assignment = create_assignment(db_session, teacher)

    repository = AssignmentDeadlineReminderRepository(db_session)

    with pytest.raises(IntegrityError):
        for i in range(2):
            repository.create(assignment_id=assignment.id, student_id=student.id, reminder_type='24_hours_before')


























