from backend.tests.test_assignment_submission_repository import create_test_environment
from backend.app.models.assignment_submission import AssignmentSubmission
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.services.assignment_submission_service import AssignmentSubmissionService
from backend.app.schemas.assignment_submission import AssignmentSubmissionCreate
import uuid
import pytest
from datetime import datetime, timezone, timedelta


def create_submission_service(db_session, submission_repository: AssignmentSubmissionRepository) -> AssignmentSubmissionService:

    enrollment_repository = CourseEnrollmentRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)

    return AssignmentSubmissionService(submission_repository=submission_repository, enrollment_repository=enrollment_repository, assignment_repository=assignment_repository)

def create_submission(submission_service: AssignmentSubmissionService, student_id: int, assignment_id: int) -> AssignmentSubmission:

    submission_data = AssignmentSubmissionCreate(content='Test Assignment Submission Content')

    return submission_service.create_submission(submission_data=submission_data, student_id=student_id, assignment_id=assignment_id)

def create_grade_test_environment(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    service = create_submission_service(db_session, submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    return submission, service, submission_repository




def test_student_can_create_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    assignment_repository = AssignmentRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    submission_service = AssignmentSubmissionService(assignment_repository=assignment_repository, enrollment_repository=enrollment_repository, submission_repository=submission_repository)

    uid = uuid.uuid4().hex[:8]

    submission_data = AssignmentSubmissionCreate(content=f'Test Assignment Submission Content {uid}')
    submission = submission_service.create_submission(submission_data=submission_data, student_id=student_id, assignment_id=assignment_id)

    assert submission is not None
    assert submission.assignment_id == assignment_id
    assert submission.student_id == student_id

def test_student_cannot_submit_to_missing_assignment(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)

    submission_service = AssignmentSubmissionService(assignment_repository=assignment_repository, enrollment_repository=enrollment_repository, submission_repository=submission_repository)

    submission_data = AssignmentSubmissionCreate(content='Test Assignment Submission Content')

    with pytest.raises(ValueError, match='Assignment not found'):
        submission_service.create_submission(assignment_id=999999, submission_data=submission_data, student_id=student_id)


def test_student_cannot_submit_without_enrollment(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session, do_not_enroll_student=True)

    enrollment_repository = CourseEnrollmentRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)

    submission_service = AssignmentSubmissionService(assignment_repository=assignment_repository, enrollment_repository=enrollment_repository, submission_repository=submission_repository)

    submission_data = AssignmentSubmissionCreate(content='Test Assignment Submission Content')

    with pytest.raises(ValueError, match='Student is not enrolled to this course'):
        submission_service.create_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)


def test_student_cannot_submit_twice(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    enrollment_repository = CourseEnrollmentRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)

    submission_service = AssignmentSubmissionService(assignment_repository=assignment_repository, enrollment_repository=enrollment_repository, submission_repository=submission_repository)

    submission_data = AssignmentSubmissionCreate(content='Test Assignment Submission Content')

    submission_service.create_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)

    with pytest.raises(ValueError, match='This assignment is already submitted'):
        submission_service.create_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)


def test_student_cannot_submit_after_deadline(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    enrollment_repository = CourseEnrollmentRepository(db_session)
    assignment_repository = AssignmentRepository(db_session)

    submission_service = AssignmentSubmissionService(enrollment_repository=enrollment_repository, submission_repository=submission_repository, assignment_repository=assignment_repository)

    assignment = assignment_repository.get_by_id(assignment_id)
    past_due_date = datetime.now(timezone.utc) - timedelta(days=1)
    assignment.due_at = past_due_date
    updated_assignment = assignment_repository.update(assignment)
    assert updated_assignment.due_at == past_due_date

    submission_data = AssignmentSubmissionCreate(content='Test Assignment Submission Content')

    with pytest.raises(ValueError, match='Assignment has expired'):
        submission_service.create_submission(assignment_id=updated_assignment.id, submission_data=submission_data, student_id=student_id)

def test_student_can_get_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    submission_service = create_submission_service(db_session, submission_repository)

    submission = create_submission(submission_service=submission_service, student_id=student_id, assignment_id=assignment_id)

    retrieved_submission = submission_service.get_submission(submission_id=submission.id)

    assert retrieved_submission.id == submission.id

def test_student_can_list_own_submissions(db_session):
    student_one_id, student_one_assignment_one_id, student_one_assignment_two_id, submission_repository = create_test_environment(db_session, create_two_assignments=True)
    student_two_id, student_two_assignment_one_id, student_two_assignment_two_id, submission_repository = create_test_environment(db_session, create_two_assignments=True)

    submission_service = create_submission_service(db_session, submission_repository)

    create_submission(submission_service=submission_service, student_id=student_one_id, assignment_id=student_one_assignment_one_id)
    create_submission(submission_service=submission_service, student_id=student_one_id, assignment_id=student_one_assignment_two_id)

    create_submission(submission_service=submission_service, student_id=student_two_id, assignment_id=student_two_assignment_one_id)
    create_submission(submission_service=submission_service, student_id=student_two_id, assignment_id=student_two_assignment_two_id)


    student_one_submissions = submission_service.list_student_submissions(student_id=student_one_id)
    student_two_submissions = submission_service.list_student_submissions(student_id=student_two_id)

    assert len(student_one_submissions) == len(student_two_submissions)
    assert len(student_one_submissions) == 2
    assert len(student_two_submissions) == 2

def test_list_assignment_submissions(db_session):
    student_one_id, student_one_assignment_one_id, student_one_assignment_two_id, submission_repository = create_test_environment(db_session, create_two_assignments=True)
    student_two_id, student_two_assignment_one_id, student_two_assignment_two_id, submission_repository = create_test_environment(db_session, create_two_assignments=True)

    submission_service = create_submission_service(db_session, submission_repository)

    student_one_assignments = [student_one_assignment_one_id, student_one_assignment_two_id]
    student_two_assignments = [student_two_assignment_one_id, student_two_assignment_two_id]

    for assignment_id in student_one_assignments:
        create_submission(submission_service=submission_service, student_id=student_one_id, assignment_id=assignment_id)


    for assignment_id in student_two_assignments:
        create_submission(submission_service=submission_service, student_id=student_two_id, assignment_id=assignment_id)


    all_assignments = [student_one_assignment_one_id, student_two_assignment_one_id, student_two_assignment_one_id, student_two_assignment_two_id]
    submissions_per_assignment = []

    for assignment_id in all_assignments:
        assignment_submissions = {f'Assignment submissions {assignment_id}': submission_service.list_assignment_submissions(assignment_id=assignment_id)}

        submissions_per_assignment.append(assignment_submissions)

    assert len(submissions_per_assignment) == len(all_assignments)
    assert len(submissions_per_assignment[0][f'Assignment submissions {student_one_assignment_one_id}']) == 1

def test_student_can_update_submission_before_deadline(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    submission_service = create_submission_service(db_session, submission_repository)

    due_date = datetime.now(timezone.utc) + timedelta(days=1)

    assignment_repository = AssignmentRepository(db_session)

    assignment = assignment_repository.get_by_id(assignment_id)
    assignment.due_at = due_date
    updated_assignment = assignment_repository.update(assignment)

    assert updated_assignment.due_at == due_date

    create_submission(submission_service=submission_service, student_id=student_id, assignment_id=assignment_id)

    submission_data = AssignmentSubmissionCreate(content='New Assignment Submission Content')

    updated_submission = submission_service.update_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)

    assert updated_submission.content == 'New Assignment Submission Content'

def test_student_cannot_update_another_students_submission(db_session):
    student_one_id, assignment_one_id, submission_repository = create_test_environment(db_session)
    student_two_id, assignment_two_id, submission_repository = create_test_environment(db_session)

    submission_service = create_submission_service(db_session, submission_repository)

    create_submission(submission_service=submission_service, student_id=student_one_id, assignment_id=assignment_one_id)
    create_submission(submission_service=submission_service, student_id=student_two_id, assignment_id=assignment_two_id)

    submission_data = AssignmentSubmissionCreate(content='New Assignment Submission Content')

    with pytest.raises(ValueError, match='Submission not found'):
        submission_service.update_submission(assignment_id=assignment_one_id, student_id=student_two_id, submission_data=submission_data)

def test_student_cannot_update_graded_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    submission_service = create_submission_service(db_session, submission_repository)

    submission = create_submission(submission_service=submission_service, student_id=student_id, assignment_id=assignment_id)

    submission.grade = 5
    submission.graded_at = datetime.now(timezone.utc)

    graded_submission = submission_repository.update(submission)

    assert graded_submission.grade == 5

    submission_data = AssignmentSubmissionCreate(content='New Assignment Submission Content')

    with pytest.raises(ValueError, match='This assignment has already been graded'):
        submission_service.update_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)

def test_student_cannot_update_after_deadline(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    submission_service = create_submission_service(db_session, submission_repository)

    assignment_repository = AssignmentRepository(db_session)

    assignment = assignment_repository.get_by_id(assignment_id)
    assignment.due_at = datetime.now(timezone.utc) - timedelta(days=1)

    assignment_repository.update(assignment)

    submission_data = AssignmentSubmissionCreate(content='New Assignment Submission Content')

    with pytest.raises(ValueError, match='Assignment has expired'):
        submission_service.update_submission(assignment_id=assignment_id, submission_data=submission_data, student_id=student_id)


def test_teacher_can_grade_submission(db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    submission_service = create_submission_service(db_session, submission_repository)

    submission = create_submission(submission_service=submission_service, student_id=student_id, assignment_id=assignment_id)

    graded_submission = submission_service.grade_submission(submission=submission, grade=50, feedback='You can do better!')

    assert graded_submission is not None
    assert graded_submission.grade == 50
    assert graded_submission.feedback == 'You can do better!'

def test_grade_can_be_zero(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    graded_submission = service.grade_submission(submission=submission, grade=0, feedback='You should try to do better!')

    assert graded_submission is not None
    assert graded_submission.grade == 0
    assert graded_submission.feedback == 'You should try to do better!'

def test_grade_can_be_100(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    graded_submission = service.grade_submission(submission=submission, grade=100, feedback='Excellent!')

    assert graded_submission is not None
    assert graded_submission.grade == 100
    assert graded_submission.feedback == 'Excellent!'

def test_grade_below_zero_is_rejected(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    with pytest.raises(ValueError, match='Grade must be between 0 and 100'):
        service.grade_submission(submission=submission, grade=-10, feedback='Try again!')

def test_grade_above_100_is_rejected(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    with pytest.raises(ValueError, match='Grade must be between 0 and 100'):
        service.grade_submission(submission=submission, grade=101, feedback='Magnificent!')

def test_cannot_grade_submission_twice(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    with pytest.raises(ValueError, match='This submission has already been graded'):
        for _ in range(2):
            service.grade_submission(submission=submission, grade=100, feedback='Excellent!')

def test_grading_sets_graded_at(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    assert submission.graded_at is None

    graded_submission = service.grade_submission(submission=submission, grade=100, feedback='Magnificent!')

    assert graded_submission.graded_at is not None

def test_feedback_can_be_empty(db_session):
    submission, service, repository = create_grade_test_environment(db_session)

    graded_submission = service.grade_submission(submission=submission, grade=100)

    assert graded_submission.feedback is None
































