from backend.app.models.user import User, UserRole
from backend.app.core.security import hash_password

def create_test_user(db_session, email: str, role: UserRole) -> User:
    user = User(email=email, role=role, hashed_password=hash_password('StrongPassword123!'), full_name='Test User')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def get_access_token(client, email: str) -> str:
    response = client.post('/auth/login', data={'username': email, 'password': 'StrongPassword123!'})
    assert response.status_code == 200
    access_token = response.json()['access_token']

    return access_token

def create_course(client, token: str) -> int:
    response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Test Course', 'content': 'Course for Course Enrollment API tests'})
    assert response.status_code == 201

    return response.json()['id']


def test_student_can_enroll_in_course(client, db_session):
    student = create_test_user(db_session, email='random_student_for_testing_enrollments@example.com', role=UserRole.STUDENT)
    teacher = create_test_user(db_session, 'random_teacher_for_testing_enrollments@example.com', role=UserRole.TEACHER)

    student_token = get_access_token(client, student.email)
    teacher_token = get_access_token(client, teacher.email)

    course_id = create_course(client, teacher_token)

    response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert response.status_code == 201


def test_teacher_cannot_enroll_in_course(client, db_session):
    teacher = create_test_user(db_session, email='teacher_cannot_enroll_in_course@example.com', role=UserRole.TEACHER)
    token = get_access_token(client, teacher.email)

    course_id = create_course(client, token)

    response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403

def test_admin_cannot_enroll_in_course(client, db_session):
    admin = create_test_user(db_session, 'admin_cannot_enroll_in_course@example.com', role=UserRole.ADMIN)
    token = get_access_token(client, admin.email)

    course_id = create_course(client, token)

    response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403


def test_student_cannot_enroll_in_missing_course(client, db_session):
    student = create_test_user(db_session, 'student_cannot_enroll_in_missing_course@example.com', role=UserRole.STUDENT)
    token = get_access_token(client, student.email)

    response = client.post('/enrollments/courses/999999/enroll', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400


def test_student_cannot_enroll_twice(client, db_session):
    teacher = create_test_user(db_session, 'teacher_that_creates_course_unenrollable_twice@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'student_that_cannot_enroll_in_course_twice@example.com', role=UserRole.STUDENT)
    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    first_response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})
    assert first_response.status_code == 201

    second_response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})
    assert second_response.status_code == 400

def test_student_can_get_his_enrollments(client, db_session):
    teacher = create_test_user(db_session, 'teacher_creates_two_courses@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'student_that_will_enroll_and_watch_his_enrollments@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    first_course_id = create_course(client, teacher_token)
    second_course_id = create_course(client, teacher_token)

    first_enrollment_response = client.post(f'/enrollments/courses/{first_course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert first_enrollment_response.status_code == 201

    second_enrollment_response = client.post(f'/enrollments/courses/{second_course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert second_enrollment_response.status_code == 201

    response = client.get('/enrollments/me', headers={'Authorization': f'Bearer {student_token}'})
    assert response.status_code == 200

    enrollments = response.json()

    assert enrollments[0]['student_id'] == student.id
    assert enrollments[0]['course_id'] == first_course_id
    assert enrollments[1]['student_id'] == student.id
    assert enrollments[1]['course_id'] == second_course_id

def test_teacher_cannot_get_my_enrollments(client, db_session):
    teacher = create_test_user(db_session, 'teacher_cannot_get_my_courses@example.com', role=UserRole.TEACHER)

    teacher_token = get_access_token(client, teacher.email)

    response = client.get('/enrollments/me', headers={'Authorization': f'Bearer {teacher_token}'})

    assert response.status_code == 403

def test_student_can_unenroll_from_course(client, db_session):
    teacher = create_test_user(db_session, 'teacher_creating_course@example.com', role=UserRole.TEACHER)
    teacher_token = get_access_token(client, teacher.email)
    student = create_test_user(db_session, 'student_can_unenroll_from_course@example.com', role=UserRole.STUDENT)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    enrollment_response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})
    assert enrollment_response.status_code == 201

    unenrollment_response = client.delete(f'/enrollments/courses/{course_id}/unenroll', headers={'Authorization': f'Bearer {student_token}'})

    assert unenrollment_response.status_code == 204

def test_student_cannot_unenroll_from_missing_course(client, db_session):
    student = create_test_user(db_session, 'student_cannot_unenroll_from_missing_course@example.com', role=UserRole.STUDENT)
    student_token = get_access_token(client, student.email)

    unenrollment_attempt_response = client.delete('/enrollments/courses/999999/unenroll', headers={'Authorization': f'Bearer {student_token}'})
    assert unenrollment_attempt_response.status_code == 400

# authentication test

def test_unauthenticated_user_cannot_enroll(client, db_session):

    teacher = create_test_user(db_session, 'teacher_creating_courses_accessible_only_for_authenticated_users@example.com', role=UserRole.TEACHER)
    teacher_token = get_access_token(client, teacher.email)

    course_id = create_course(client, teacher_token)

    response = client.post(f'/enrollments/courses/{course_id}/enroll')
    assert response.status_code == 401





