from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.assignment_repository import AssignmentRepository

from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.assignment import Assignment

from backend.app.core.security import hash_password
import uuid
import pytest


def create_test_environment(db_session):
    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    assignment_repository = AssignmentRepository(db_session)

    uid = uuid.uuid4().hex[:8]
    default_password = 'SuperSecretPassword123!'

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password(default_password), role=UserRole.TEACHER, full_name='Test User'))
    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=user.id))
    course = course_service.publish_course(course.id)


    return user, course, assignment_repository

def create_test_user(db_session, role: UserRole) -> User:

    user_repository = UserRepository(db_session)

    uid = uuid.uuid4().hex[:8]

    default_password = 'SuperSecretPassword123!'

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password(default_password), role=role, full_name='Test User'))

    return user

def test_create_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)
    uid = uuid.uuid4().hex[:8]

    assignment = assignment_repository.create(Assignment(title=f'Test Assignment {uid}', description='Test Assignment Description', course_id=course.id))

    assert assignment.course_id == course.id
    assert assignment.description == 'Test Assignment Description'
    assert assignment.due_at is None

def test_get_assignment_by_id(db_session):
    user, course, assignment_repository = create_test_environment(db_session)

    uid = uuid.uuid4().hex[:8]

    assignment = assignment_repository.create(Assignment(title=f'Test Assignment {uid}', description='Test Assignment Description', course_id=course.id))

    assert assignment.course_id == course.id

    retrieved_assignment = assignment_repository.get_by_id(assignment.id)

    assert retrieved_assignment.id == assignment.id
    assert retrieved_assignment.course_id == course.id

def test_get_assignment_by_id_returns_none_for_missing_assignment(db_session):
    assignment_repository = AssignmentRepository(db_session)

    retrieved_assignment = assignment_repository.get_by_id(999999)

    assert retrieved_assignment is None

def test_list_assignments_by_course(db_session):
    user_a, course_a, assignment_repository = create_test_environment(db_session)
    user_b, course_b, assignment_repository = create_test_environment(db_session)

    assignment_repository.create(Assignment(title=f'Assignment one {course_a.id}', description='Assignment one description', course_id=course_a.id))
    assignment_repository.create(Assignment(title=f'Assignment two {course_a.id}', description='Assignment two description', course_id=course_a.id))

    assignment_repository.create(Assignment(title=f'Assignment One {course_b.id}', description='Assignment One description', course_id=course_b.id))

    course_a_assignments = assignment_repository.list_by_course(course_a.id)
    course_b_assignments = assignment_repository.list_by_course(course_b.id)

    assert len(course_a_assignments) == 2
    assert len(course_b_assignments) == 1




def test_list_assignments_by_course_returns_empty_list(db_session):
    user, course, assignment_repository = create_test_environment(db_session)

    course_assignments = assignment_repository.list_by_course(course.id)

    assert len(course_assignments) == 0

def test_update_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)

    assignment = assignment_repository.create(Assignment(title=f'Assignment {uuid.uuid4().hex[:8]}', description='Test Assignment Description', course_id=course.id))

    assignment.title = 'New Assignment Title'

    updated_assignment = assignment_repository.update(assignment)

    assert updated_assignment.title == 'New Assignment Title'

def test_delete_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)

    assignment = assignment_repository.create(Assignment(title=f'Test Assignment {uuid.uuid4().hex[:8]}', description='Test Assignment Description', course_id=course.id))

    assignment_repository.delete(assignment)

    course_assignments = assignment_repository.list_by_course(course.id)

    assert len(course_assignments) == 0






