from backend.tests.test_assignment_repository import create_test_environment as cte, create_test_user
from backend.app.models.assignment_submission import AssignmentSubmission
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.models.assignment import Assignment
from backend.app.models.user import UserRole
from sqlalchemy.exc import IntegrityError
from typing import Optional
import uuid
import pytest

def create_test_environment(db_session, do_not_enroll_student: Optional[bool] = False, create_two_assignments: Optional[bool] = False, include_teacher: Optional[bool] = False):
    user, course, assignment_repository = cte(db_session)

    enrollment_repository = CourseEnrollmentRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

    uid = uuid.uuid4().hex[:8]



    student = create_test_user(db_session, role=UserRole.STUDENT)
    if do_not_enroll_student == False:
        enrollment_service.enroll(student_id=student.id, course_id=course.id)

    submission_repository = AssignmentSubmissionRepository(db_session)

    if create_two_assignments == True:
        assignment_one = assignment_repository.create(
            Assignment(title=f'Test Assignment {uuid.uuid4().hex[:8]}', course_id=course.id))
        assignment_two = assignment_repository.create(
            Assignment(title=f'Test Assignment {uuid.uuid4().hex[:8]}', course_id=course.id))

        if include_teacher:
            return student.id, assignment_one.id, assignment_two.id, submission_repository, user
        else:
            return student.id, assignment_one.id, assignment_two.id, submission_repository
    else:

        assignment = assignment_repository.create(Assignment(title=f'Test Assignment {uid}', course_id=course.id))
        if include_teacher:
            return student.id, assignment.id, submission_repository, user
        else:
            return student.id, assignment.id, submission_repository

def create_assignment_submission(student_id: int, assignment_id: int, submission_repository: AssignmentSubmissionRepository):
    assignment_submission = submission_repository.create(AssignmentSubmission(student_id=student_id, assignment_id=assignment_id, content='Test Submission Content'))

    return assignment_submission


def test_create_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    assignment_submission = submission_repository.create(AssignmentSubmission(content='Test Submission Content', assignment_id=assignment_id, student_id=student_id))

    assert assignment_submission is not None
    assert assignment_submission.assignment_id == assignment_id
    assert assignment_submission.student_id == student_id

def test_get_submission_by_id(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    assignment_submission = create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)

    retrieved_submission = submission_repository.get_by_id(assignment_submission.id)

    assert retrieved_submission.assignment_id == assignment_id

def test_get_submission_by_id_returns_none_for_missing_submission(db_session):
    submission_repository = AssignmentSubmissionRepository(db_session)

    retrieved_submission = submission_repository.get_by_id(999999)

    assert retrieved_submission is None

def test_get_submission_by_student_and_assignment(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    assignment_submission = create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)

    retrieved_submission = submission_repository.get_by_student_and_assignment(assignment_id=assignment_id, student_id=student_id)

    assert retrieved_submission.id == assignment_submission.id
    assert retrieved_submission.assignment_id == assignment_submission.assignment_id
    assert retrieved_submission.student_id == assignment_submission.student_id

def test_get_submission_by_student_and_assignment_returns_none_when_missing(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    retrieved_submission = submission_repository.get_by_student_and_assignment(student_id=student_id, assignment_id=assignment_id)

    assert retrieved_submission is None

def test_list_submissions_by_assignment(db_session):
    student_one_id, assignment_id, submission_repository = create_test_environment(db_session)
    student_two = create_test_user(db_session, role=UserRole.STUDENT)
    student_three = create_test_user(db_session, role=UserRole.STUDENT)

    students_id = [student_one_id, student_two.id, student_three.id]

    for student_id in students_id:
        create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)



    assignment_submissions = submission_repository.list_by_assignment(assignment_id=assignment_id)

    assert len(assignment_submissions) == 3

def test_list_submissions_by_student(db_session):
    student_a_id, assignment_a_id, submission_repository = create_test_environment(db_session)
    student_b_id, assignment_b_id, submission_repository = create_test_environment(db_session)


    create_assignment_submission(student_id=student_a_id, assignment_id=assignment_a_id, submission_repository=submission_repository)
    create_assignment_submission(student_id=student_b_id, assignment_id=assignment_b_id, submission_repository=submission_repository)



    student_a_assignments = submission_repository.list_by_student(student_id=student_a_id)
    student_b_assignments = submission_repository.list_by_student(student_id=student_b_id)

    assert len(student_a_assignments) == 1
    assert len(student_b_assignments) == 1

def test_update_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    assignment_submission = create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)

    assignment_submission.content = 'Updated Submission Content'

    updated_submission = submission_repository.update(assignment_submission)

    assert updated_submission.content == 'Updated Submission Content'

def test_unique_student_assignment_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)

    with pytest.raises(IntegrityError):
        create_assignment_submission(student_id=student_id, assignment_id=assignment_id, submission_repository=submission_repository)




















