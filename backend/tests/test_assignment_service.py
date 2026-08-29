from backend.tests.test_assignment_repository import create_test_environment, create_test_user
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.services.assignment_service import AssignmentService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.assignment import AssignmentCreate
import pytest
import uuid


def test_create_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)
    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)
    uid = uuid.uuid4().hex[:8]

    assignment_data = AssignmentCreate(title=f'Test Assignment {uid}', description='Test Assignment Description')

    assignment = assignment_service.create_assignment(assignment_data=assignment_data, course_id=course.id)

    assert assignment is not None
    assert assignment.course_id == course.id
    assert assignment.title == assignment_data.title
    assert assignment.description == assignment_data.description

def test_get_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)
    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)
    uid = uuid.uuid4().hex[:8]

    assignment = assignment_service.create_assignment(assignment_data=AssignmentCreate(title=f'Test Assignment {uid}'), course_id=course.id)

    assert assignment is not None
    assert assignment.course_id == course.id

    retrieved_assignment = assignment_service.get_assignment(assignment_id=assignment.id)

    assert retrieved_assignment is not None
    assert retrieved_assignment.id == assignment.id

def test_get_missing_assignment(db_session):
    assignment_repository = AssignmentRepository(db_session)
    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Assignment not found'):
            assignment_service.get_assignment(assignment_id=999999)


def test_list_course_assignments(db_session):
    user_a, course_a, assignment_repository = create_test_environment(db_session)
    user_b, course_b, assignment_repository = create_test_environment(db_session)

    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)

    for i in range(2):
        assignment_data = AssignmentCreate(title=f'Test Assignment {i}')
        assignment_service.create_assignment(assignment_data=assignment_data, course_id=course_a.id)


    for i in range(2):
        assignment_data = AssignmentCreate(title=f'Test Assignment {i + 1}')
        assignment_service.create_assignment(assignment_data=assignment_data, course_id=course_b.id)


    course_a_assignments = assignment_service.list_course_assignments(course_id=course_a.id)
    course_b_assignments = assignment_service.list_course_assignments(course_id=course_b.id)

    assert len(course_a_assignments) == len(course_b_assignments)

def test_list_assignments_for_missing_course(db_session):
    course_repository = CourseRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)

    with pytest.raises(ValueError, match='Course not found'):
        assignment_service.list_course_assignments(999999)

def test_update_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)
    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)

    uid = uuid.uuid4().hex[:8]

    assignment_data = AssignmentCreate(title=f'Test Assignment {uid}')

    assignment = assignment_service.create_assignment(assignment_data=assignment_data, course_id=course.id)

    updated_assignment = assignment_service.update_assignment(assignment=assignment, assignment_data=AssignmentCreate(title=f'Updated Assignment {uid}'))

    assert updated_assignment is not None
    assert updated_assignment.title == f'Updated Assignment {uid}'

def test_delete_assignment(db_session):
    user, course, assignment_repository = create_test_environment(db_session)
    course_repository = CourseRepository(db_session)
    assignment_service = AssignmentService(repository=assignment_repository, course_repository=course_repository)

    uid = uuid.uuid4().hex[:8]

    assignment_data = AssignmentCreate(title=f'Test Assignment {uid}')
    assignment = assignment_service.create_assignment(assignment_data=assignment_data, course_id=course.id)

    deleted_assignment = assignment_service.delete_assignment(assignment=assignment)

    assert deleted_assignment is None

    course_assignments = assignment_service.list_course_assignments(course_id=course.id)

    assert len(course_assignments) == 0











