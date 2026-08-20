from backend.app.models.user import User, UserRole
from backend.app.models.course import CourseStatus
from backend.app.core.security import hash_password


def get_access_token(client, email):
    response = client.post('/auth/login', data={'username': email, 'password': 'StrongPassword123!'})

    assert response.status_code == 200

    return response.json()['access_token']

def create_test_user(db_session, email: str, role: UserRole) -> User:
    user = User(email=email, hashed_password=hash_password('StrongPassword123!'), full_name='Test User', role=role)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def test_teacher_can_create_course(client, db_session):
    teacher = create_test_user(db_session, email='teacher_courses@example.com', role=UserRole.TEACHER)

    token = get_access_token(client, teacher.email)

    response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Python Programming', 'description': 'Introduction to Python'})

    assert response.status_code == 201

    data = response.json()

    assert data['title'] == 'Python Programming'
    assert data['description'] == 'Introduction to Python'
    assert data['teacher_id'] == teacher.id


def test_student_cannot_create_course(client, db_session):

    student = create_test_user(db_session, email='student_courses@example.com', role=UserRole.STUDENT)

    token = get_access_token(client, student.email)

    response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Python Programming', 'description': 'Introduction to Python'})

    assert response.status_code == 403

def test_admin_can_create_course(client, db_session):

    admin = create_test_user(db_session, email='admin_courses@example.com', role=UserRole.ADMIN)

    token = get_access_token(client, admin.email)

    response = client.post('courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Some admin course', 'description': 'Introduction to FastAPI'})
    assert response.status_code == 201

    data = response.json()

    assert data['title'] == 'Some admin course'
    assert data['description'] == 'Introduction to FastAPI'
    assert data['teacher_id'] == admin.id

def test_list_courses(client, db_session):
    teacher = create_test_user(db_session, email='list_courses_teacher@example.com', role=UserRole.TEACHER)

    token = get_access_token(client, teacher.email)

    first_response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Python Basics', 'description': 'Learn Python fundamentals'})
    assert first_response.status_code == 201

    second_response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Advanced Python', 'description': 'Advanced Python concepts.'})

    assert second_response.status_code == 201

    response = client.get('/courses')

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]['title'] == 'Advanced Python'
    assert data[1]['title'] == 'Python Basics'


def test_teacher_can_list_my_courses(client, db_session):
    teacher = create_test_user(db_session, 'my_courses_teacher@example.com', UserRole.TEACHER)
    token = get_access_token(client, teacher.email)

    response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'My Course', 'description': 'A course owned by this teacher.'})

    assert response.status_code == 201

    response = client.get('/courses/my', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]['title'] == 'My Course'
    assert data[0]['teacher_id'] == teacher.id


def test_student_cannot_list_my_courses(client, db_session):
    student = create_test_user(db_session, 'my_courses_student@example.com', UserRole.STUDENT)
    token = get_access_token(client, student.email)

    response = client.get('/courses/my', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


def test_get_course(client, db_session):
    teacher = create_test_user(db_session, 'get_course_teacher@example.com', UserRole.TEACHER)
    token = get_access_token(client, teacher.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Course Details', 'description': 'Course details test.'})

    assert create_response.status_code == 201

    course_id = create_response.json()['id']

    response = client.get(f'/courses/{course_id}')

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == course_id
    assert data['title'] == 'Course Details'
    assert data['description'] == 'Course details test.'


def test_get_missing_course(client):
    response = client.get('/courses/999999')

    assert response.status_code == 404

def test_teacher_can_publish_own_course(client, db_session):
    teacher = create_test_user(db_session, 'test_teacher_can_publish_own_course@example.com', UserRole.TEACHER)

    token = get_access_token(client, teacher.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'A course for publishing', 'description': 'A course that is going to be published by the teacher.'})

    assert create_response.status_code == 201

    data = create_response.json()


    assert data['title'] == 'A course for publishing'

    course_id = data['id']

    publish_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {token}'})

    assert publish_response.status_code == 200

    data = publish_response.json()

    assert data['status'] == CourseStatus.PUBLISHED


def test_admin_can_publish_course(client, db_session):
    teacher = create_test_user(db_session, 'test_admin_can_publish_teachers+course@example.com', UserRole.TEACHER)
    admin = create_test_user(db_session, 'test_admin_is_allowed_to_do_everything@example.com', UserRole.ADMIN)

    teacher_token = get_access_token(client, teacher.email)
    admin_token = get_access_token(client, admin.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A course publishable for admins', 'description': 'Courses can be published by admins as well.'})

    assert create_response.status_code == 201

    data = create_response.json()

    assert data['title'] == 'A course publishable for admins'

    course_id = data['id']

    publish_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {admin_token}'})

    assert publish_response.status_code == 200

    data = publish_response.json()

    assert data['status'] == CourseStatus.PUBLISHED

def test_teacher_cannot_publish_other_teachers_course(client, db_session):
    teacher_a = create_test_user(db_session, 'teacher_a@example.com', UserRole.TEACHER)
    teacher_b = create_test_user(db_session, 'teacher_b@example.com', UserRole.TEACHER)

    teacher_a_token = get_access_token(client, teacher_a.email)
    teacher_b_token = get_access_token(client, teacher_b.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_a_token}'}, json={'title': 'A course for TEACHER B', 'description': 'Created by TEACHER A.'})
    assert create_response.status_code == 201

    data = create_response.json()

    assert data['title'] == 'A course for TEACHER B'

    course_id = data['id']

    publish_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_b_token}'})

    assert publish_response.status_code == 403


def test_student_cannot_publish_course(client, db_session):
    teacher = create_test_user(db_session, 'test_student_cannot_publish_course@example.com', UserRole.TEACHER)
    student = create_test_user(db_session, 'the_student_that_cannot_publish_other_teachers_course@example.com', UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A course for the student\'s failed attempt to get it published', 'description': 'This course should not be published by the student.'})

    assert create_response.status_code == 201

    data = create_response.json()

    assert data['title'] == 'A course for the student\'s failed attempt to get it published'

    course_id = data['id']

    publish_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {student_token}'})

    assert publish_response.status_code == 403

def test_publish_missing_course(client, db_session):

    teacher = create_test_user(db_session, 'test_publish_missing_course@example.com', UserRole.TEACHER)

    teacher_token = get_access_token(client, teacher.email)

    publish_response = client.post('/courses/999999/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_response.status_code == 404


def test_cannot_publish_already_published_course(client, db_session):
    teacher = create_test_user(db_session, 'test_teacher_cannot_publish_already_published_course@example.com', UserRole.TEACHER)
    teacher_token = get_access_token(client, teacher.email)

    create_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A course that should not be published twice', 'description': 'This course should not be published twice'})

    assert create_response.status_code == 201

    data = create_response.json()

    assert data['title'] == 'A course that should not be published twice'

    course_id = data['id']

    publish_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_response.status_code == 200

    data = publish_response.json()

    assert data['status'] == CourseStatus.PUBLISHED

    published_course_id = data['id']

    assert published_course_id == course_id

    second_publish_attempt_response = client.post(f'courses/{published_course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert second_publish_attempt_response.status_code == 400

    data = second_publish_attempt_response.json()

    assert data['detail'] == 'Only draft courses can be published'


def test_student_can_get_course_progress(client, db_session):
    teacher = create_test_user(db_session, email='test_student_can_get_course_progress_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_can_get_course_progress@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    create_course_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A course for STUDENT to view his own progress', 'description': 'Student ACTUALLY can view his course progress'})
    assert create_course_response.status_code == 201

    data = create_course_response.json()

    assert data is not None
    assert data['status'] == CourseStatus.DRAFT

    course_id = data['id']


    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    data = publish_course_response.json()

    assert data is not None
    assert data['status'] == CourseStatus.PUBLISHED

    published_course_id = data['id']

    assert published_course_id == course_id

    create_lesson_one_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Lesson one', 'content': 'Lesson one content'})

    assert create_lesson_one_response.status_code == 201

    lesson_one_data = create_lesson_one_response.json()
    assert lesson_one_data is not None
    assert lesson_one_data['course_id'] == published_course_id

    lesson_one_id = lesson_one_data['id']

    create_lesson_two_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Lesson two', 'content': 'Lesson two content'})
    assert create_lesson_two_response.status_code == 201

    lesson_two_data = create_lesson_two_response.json()

    assert lesson_two_data is not None
    assert lesson_two_data['course_id'] == published_course_id

    lesson_two_id = lesson_two_data['id']

    create_lesson_three_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Lesson three', 'content': 'Lesson three content'})

    assert create_lesson_three_response.status_code == 201

    lesson_three_data = create_lesson_three_response.json()

    assert lesson_three_data is not None
    assert lesson_three_data['course_id'] == published_course_id

    lesson_three_id = lesson_three_data['id']

    create_lesson_four_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Lesson four', 'content': 'Lesson four content'})
    assert create_lesson_four_response.status_code == 201

    lesson_four_data = create_lesson_four_response.json()

    assert lesson_four_data is not None
    assert lesson_four_data['course_id'] == published_course_id

    lesson_four_id = lesson_four_data['id']

    student_course_enrollment_response = client.post(f'/enrollments/courses/{published_course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert student_course_enrollment_response.status_code == 201

    student_course_enrollment_data = student_course_enrollment_response.json()

    assert student_course_enrollment_data is not None
    assert student_course_enrollment_data['course_id'] == published_course_id
    assert student_course_enrollment_data['student_id'] == student.id

    student_marks_lesson_one_complete_response = client.post(f'/lessons/{lesson_one_id}/complete', headers={'Authorization': f'Bearer {student_token}'})

    assert student_marks_lesson_one_complete_response.status_code == 201

    completed_lesson_one_data = student_marks_lesson_one_complete_response.json()

    assert completed_lesson_one_data is not None
    assert completed_lesson_one_data['lesson_id'] == lesson_one_id
    assert completed_lesson_one_data['student_id'] == student.id

    student_marks_lesson_two_complete_response = client.post(f'/lessons/{lesson_two_id}/complete', headers={'Authorization': f'Bearer {student_token}'})
    assert student_marks_lesson_two_complete_response.status_code == 201

    completed_lesson_two_data = student_marks_lesson_two_complete_response.json()

    assert completed_lesson_two_data is not None
    assert completed_lesson_two_data['lesson_id'] == lesson_two_id
    assert completed_lesson_two_data['student_id'] == student.id

    student_gets_course_progress_response = client.get(f'/courses/{course_id}/progress', headers={'Authorization': f'Bearer {student_token}'})

    assert student_gets_course_progress_response.status_code == 200

    students_received_progress_data = student_gets_course_progress_response.json()

    assert students_received_progress_data is not None
    assert students_received_progress_data['course_id'] == published_course_id
    assert students_received_progress_data['total_lessons'] == 4
    assert students_received_progress_data['completed_lessons'] == 2
    assert students_received_progress_data['progress_percentage'] == 50.0


def test_unenrolled_student_cannot_get_course_progress(client, db_session):

    teacher = create_test_user(db_session, email='test_unenrolled_student_cannot_get_course_progress_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_is_unenrolled_and_that_is_why_he_cannot_get_his_own_course_progress@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    create_course_response = client.post('/courses', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A course that cannot be viewed by an unenrolled student', 'description': 'This course and its progress should not be viewed by unenrolled students.'})

    assert create_course_response.status_code == 201

    created_course_data = create_course_response.json()

    assert created_course_data is not None
    assert created_course_data['title'] == 'A course that cannot be viewed by an unenrolled student'
    assert created_course_data['status'] == CourseStatus.DRAFT

    created_course_id = created_course_data['id']

    publish_course_response = client.post(f'/courses/{created_course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200

    published_course_data = publish_course_response.json()

    assert published_course_data is not None
    assert published_course_data['id'] == created_course_id

    published_course_id = published_course_data['id']

    student_tries_getting_course_progress_without_enrollment_response = client.get(f'/courses/{published_course_id}/progress', headers={'Authorization': f'Bearer {student_token}'})

    assert student_tries_getting_course_progress_without_enrollment_response.status_code == 400


def test_student_cannot_get_course_progress_for_missing_course(client, db_session):

    student = create_test_user(db_session, email='this_student_cannot_get_course_progress_for_missing_course@example.com', role=UserRole.STUDENT)

    student_token = get_access_token(client, student.email)

    student_tries_to_get_progress_for_missing_course_response = client.get('/courses/999999/progress', headers={'Authorization': f'Bearer {student_token}'})

    assert student_tries_to_get_progress_for_missing_course_response.status_code == 400


def test_teacher_cannot_get_course_progress(client, db_session):
    teacher = create_test_user(db_session, email='test_teacher_cannot_get_course_progress_test_teacher@example.com', role=UserRole.TEACHER)

    teacher_token = get_access_token(client, teacher.email)

    teacher_tries_to_get_course_progress_response = client.get('/courses/999999/progress', headers={'Authorization': f'Bearer {teacher_token}'})
    assert teacher_tries_to_get_course_progress_response.status_code == 403


def test_unauthenticated_user_cannot_get_course_progress(client, db_session):

    unauthenticated_user_tries_to_get_course_progress_response = client.get('/courses/999999/progress')

    assert unauthenticated_user_tries_to_get_course_progress_response.status_code == 401
















