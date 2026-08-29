from backend.tests.test_assignment_submission_service import create_test_environment, create_submission, create_submission_service
from datetime import datetime, timezone, timedelta
from backend.tests.test_quiz_attempt_api import login_user, create_test_user_and_login
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.models.assignment import Assignment
from backend.app.models.user import UserRole


def get_token(db_session, client, student_id: int) -> str:
    user_repository = UserRepository(db_session)
    current_user = user_repository.get_by_id(student_id)
    if current_user is None:
        raise ValueError('User not found')

    token = login_user(client=client, email=current_user.email)

    return token

def get_assignment(db_session, assignment_id: int) -> Assignment:
    assignment_repository = AssignmentRepository(db_session)

    assignment = assignment_repository.get_by_id(assignment_id)

    if assignment is None:
        raise ValueError('Assignment not found')

    return assignment

def update_assignment(db_session, assignment: Assignment) -> Assignment:
    assignment_repository = AssignmentRepository(db_session)

    return assignment_repository.update(assignment)





def test_student_can_submit_assignment(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    token = get_token(db_session=db_session, client=client, student_id=student_id)

    response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 201

def test_student_cannot_submit_without_enrollment(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session, do_not_enroll_student=True)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 400

def test_student_cannot_submit_twice(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    first_response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert first_response.status_code == 201

    second_response = client.post(f'/assignments/{assignment_id}/submissions', headers={"Authorization": f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert second_response.status_code == 400

def test_student_cannot_submit_after_deadline(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    assignment = get_assignment(db_session=db_session, assignment_id=assignment_id)
    assignment.due_at = datetime.now() - timedelta(days=1)
    update_assignment(db_session=db_session, assignment=assignment)

    response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 400

def test_non_student_cannot_submit_assignment(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    admin_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.ADMIN)

    response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {admin_token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 403

def test_student_can_list_own_submissions(client, db_session):
    student_id, assignment_one_id, assignment_two_id,  submission_repository = create_test_environment(db_session, create_two_assignments=True)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    assignments = [assignment_one_id, assignment_two_id]
    responses = []

    for assignment_id in assignments:
        response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})
        responses.append(response)

    for response in responses:
        assert response.status_code == 201

    list_submissions_response = client.get('/submissions/me', headers={'Authorization': f'Bearer {token}'})

    assert list_submissions_response.status_code == 200
    assert len(list_submissions_response.json()) == 2

def test_student_can_get_own_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    create_response = client.post(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert create_response.status_code == 201
    submission_id = create_response.json()['id']





    get_response = client.get(f'/submissions/{submission_id}', headers={'Authorization': f'Bearer {token}'})

    assert get_response.status_code == 200

def test_student_cannot_get_another_students_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    another_student_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.STUDENT)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.get(f'/submissions/{submission.id}', headers={'Authorization': f'Bearer {another_student_token}'})

    assert response.status_code == 403

def test_student_can_update_own_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}', headers={"Authorization": f'Bearer {token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 200

def test_student_cannot_update_another_students_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    another_students_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.STUDENT)


    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}', headers={'Authorization': f'Bearer {another_students_token}'}, json={'content': 'Test Submission Content'})

    assert response.status_code == 403

def test_student_cannot_update_graded_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    token = get_token(db_session=db_session, client=client, student_id=student_id)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    submission.grade = 5
    submission.graded_at = datetime.now(timezone.utc)
    submission_repository.update(submission)

    response = client.put(f'/submissions/{submission.id}', headers={'Authorization': f'Bearer {token}'}, json={"content": 'Graded Submission Content'})

    assert response.status_code == 400

def test_unauthenticated_user_cannot_submit_assignment(client):

    response = client.post('/assignments/999999/submissions')

    assert response.status_code == 401

def test_unauthenticated_user_cannot_view_submissions(client):

    response = client.get('/submissions/me')

    assert response.status_code == 401

def test_teacher_can_view_assignment_submissions(client, db_session):
    student_one_id, assignment_id, submission_repository, teacher = create_test_environment(db_session, include_teacher=True)
    assignment_repository = AssignmentRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(course_repository=course_repository, enrollment_repository=enrollment_repository)

    assignment = assignment_repository.get_by_id(assignment_id)
    course = course_repository.get_by_id(assignment.course_id)

    student_two, token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.STUDENT, include_user=True)
    enrollment_service.enroll(student_id=student_two.id, course_id=course.id)


    teacher_token = login_user(client, teacher.email)
    service = create_submission_service(db_session, submission_repository=submission_repository)

    create_submission(submission_service=service, student_id=student_one_id, assignment_id=assignment_id)
    create_submission(submission_service=service, student_id=student_two.id, assignment_id=assignment_id)

    response = client.get(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {teacher_token}'})
    assert response.status_code == 200

    assert response.json()[1]['assignment_id'] == assignment_id
    assert response.json()[1]['student_id'] == student_one_id

    assert response.json()[0]['assignment_id'] == assignment_id
    assert response.json()[0]['student_id'] == student_two.id

    assert len(response.json()) == 2

def test_teacher_cannot_view_another_teachers_submissions(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)
    teacher_token = create_test_user_and_login(db_session, client=client, role=UserRole.TEACHER)

    response = client.get(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {teacher_token}'})

    assert response.status_code == 403

def test_admin_can_view_any_assignment_submissions(client, db_session):
    student_one_id, assignment_id, submission_repository = create_test_environment(db_session)
    student_two, token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.STUDENT, include_user=True)

    assignment_repository = AssignmentRepository(db_session)
    course_repository = CourseRepository(db_session)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(course_repository=course_repository, enrollment_repository=enrollment_repository)

    assignment = assignment_repository.get_by_id(assignment_id)
    course = course_repository.get_by_id(assignment.course_id)
    enrollment_service.enroll(student_id=student_two.id, course_id=course.id)

    students = [student_one_id, student_two.id]

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    for student_id in students:
        create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)


    admin_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.ADMIN)

    response = client.get(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {admin_token}'})

    assert response.status_code == 200
    assert len(response.json()) == 2


    assert response.json()[0]['assignment_id'] == assignment_id
    assert response.json()[0]['student_id'] == student_two.id

    assert response.json()[1]['assignment_id'] == assignment_id
    assert response.json()[1]['student_id'] == student_one_id


def test_student_cannot_view_teacher_submission_list(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    student_token = get_token(db_session=db_session, client=client, student_id=student_id)

    response = client.get(f'/assignments/{assignment_id}/submissions', headers={'Authorization': f'Bearer {student_token}'})

    assert response.status_code == 403

def test_teacher_can_grade_submission(client, db_session):
    student_id, assignment_id, submission_repository, teacher = create_test_environment(db_session, include_teacher=True)
    teacher_token = login_user(client, teacher.email)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)

    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {teacher_token}'}, json={'grade': 100, 'feedback': 'Excellent!'})

    assert response.status_code == 200
    assert response.json()['grade'] == 100
    assert response.json()['feedback'] == 'Excellent!'
    assert response.json()['graded_at'] is not None
    assert response.json()['submitted_at'] is not None

def test_teacher_cannot_grade_another_teachers_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    teacher_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.TEACHER)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {teacher_token}'}, json={'grade': 5, 'feedback': 'Try again!'})

    assert response.status_code == 403

def test_admin_can_grade_any_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    admin_token = create_test_user_and_login(db_session=db_session, client=client, role=UserRole.ADMIN)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {admin_token}'}, json={'grade': 100, 'feedback': 'Excellent!'})

    assert response.status_code == 200
    assert response.json()['grade'] == 100
    assert response.json()['feedback'] == 'Excellent!'
    assert response.json()['graded_at'] is not None
    assert response.json()['submitted_at'] is not None

def test_student_cannot_grade_submission(client, db_session):
    student_id, assignment_id, submission_repository = create_test_environment(db_session)

    student_token = get_token(db_session=db_session, client=client, student_id=student_id)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {student_token}'}, json={"grade": 5, 'feedback': 'Try again!'})

    assert response.status_code == 403

def test_cannot_grade_submission_twice(client, db_session):
    student_id, assignment_id, submission_repository, teacher = create_test_environment(db_session, include_teacher=True)

    teacher_token = login_user(client, teacher.email)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {teacher_token}'}, json={"grade": 5, 'feedback': 'Try again!'})

    assert response.status_code == 200

    additional_response = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {teacher_token}'}, json={'grade': 5, 'feedback': 'Try again!'})

    assert additional_response.status_code == 400

def test_invalid_grade_is_rejected(client, db_session):
    student_id, assignment_id, submission_repository, teacher = create_test_environment(db_session, include_teacher=True)
    teacher_token = login_user(client, teacher.email)

    service = create_submission_service(db_session=db_session, submission_repository=submission_repository)
    submission = create_submission(submission_service=service, student_id=student_id, assignment_id=assignment_id)

    response_one = client.put(f'/submissions/{submission.id}/grade', headers={'Authorization': f'Bearer {teacher_token}'}, json={'grade': 101, 'feedback': 'Invalid Grade!'})
    assert response_one.status_code == 400

    response_two = client.put(f'/submissions/{submission.id}/grade', headers={"Authorization": f'Bearer {teacher_token}'}, json={"grade": -1, 'feedback': 'Invalid Grade!'})

    assert response_two.status_code == 400
























