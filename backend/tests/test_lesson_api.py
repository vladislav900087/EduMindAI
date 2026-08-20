

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

    return response.json()['access_token']

# POST lessons tests
def create_course(client, token: str) -> int:
    response = client.post('/courses', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Test Course', 'description': 'Course for lesson API tests.'})

    assert response.status_code == 201

    return response.json()['id']

def test_teacher_can_create_lesson(client, db_session):
    teacher = create_test_user(db_session, 'lesson_teacher@example.com', UserRole.TEACHER)

    token = get_access_token(client, teacher.email)

    course_id = create_course(client, token)

    response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Introduction to Python', 'content': 'Python is a high-level programming language'})

    assert response.status_code == 201

    data = response.json()

    assert data['title'] == 'Introduction to Python'
    assert data['content'] == 'Python is a high-level programming language'
    assert data['course_id'] == course_id


def test_student_cannot_create_lesson(client, db_session):
    teacher = create_test_user(db_session, 'lesson_owner@example.com', UserRole.TEACHER)
    student = create_test_user(db_session, 'lesson_student@example.com', UserRole.STUDENT)
    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    response = client.post(f'courses/{course_id}/lessons', headers={'Authorization': f'Bearer {student_token}'}, json={'title': 'Forbidden Lesson', 'description': 'Students cannot create lessons.'})
    assert response.status_code == 403


def test_teacher_cannot_create_lesson_in_other_teachers_course(client, db_session):
    first_teacher = create_test_user(db_session, 'first_lesson_teacher@example.com', UserRole.TEACHER)
    second_teacher = create_test_user(db_session, 'second_lesson_teacher@example.com', UserRole.TEACHER)

    first_token = get_access_token(client, first_teacher.email)
    second_token = get_access_token(client, second_teacher.email)

    course_id = create_course(client, first_token)

    response = client.post(f'courses/{course_id}/lessons', headers={'Authorization': f'Bearer {second_token}'}, json={'title': 'Forbidden Lesson', 'content': 'Another teacher does not own this course.'})

    assert response.status_code == 403

# read lessons tests
def test_list_course_lessons(client, db_session):
    teacher = create_test_user(db_session, 'list_lessons_teacher@example.com', UserRole.TEACHER)
    token = get_access_token(client, teacher.email)
    course_id = create_course(client, token)

    first_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Lesson One', 'content': 'First Lesson.'})

    assert first_response.status_code == 201

    second_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Lesson Two', 'content': 'Second Lesson.'})
    assert second_response.status_code == 201

    response = client.get(f'/courses/{course_id}/lessons')

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]['title'] == 'Lesson One'
    assert data[1]['title'] == 'Lesson Two'
    assert data[0]['course_id'] == course_id
    assert data[1]['course_id'] == course_id


def test_get_lesson(client, db_session):
    teacher = create_test_user(db_session, 'get_lesson_teacher@example.com', UserRole.TEACHER)
    token = get_access_token(client, teacher.email)

    course_id = create_course(client, token)

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Lesson Details', 'content': 'Detailed lesson content.'})

    assert create_response.status_code == 201
    lesson_id = create_response.json()['id']

    response = client.get(f'/lessons/{lesson_id}')

    assert response.status_code == 200

    data = response.json()

    assert data['id'] == lesson_id
    assert data['title'] == 'Lesson Details'
    assert data['content'] == 'Detailed lesson content.'
    assert data['course_id'] == course_id


def test_get_missing_lesson(client):
    response = client.get('/lessons/999999')

    assert response.status_code == 404

def test_list_lessons_for_missing_course(client):
    response = client.get('/courses/999999/lessons')

    assert response.status_code == 404

# DELETE lessons tests

def test_teacher_can_delete_own_lesson(client, db_session):
    teacher = create_test_user(db_session, 'delete_lesson_teacher@example.com', UserRole.TEACHER)
    token = get_access_token(client, teacher.email)
    course_id = create_course(client, token)

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Lesson To Delete', 'content': 'This lesson will be deleted.'})
    assert create_response.status_code == 201

    lesson_id = create_response.json()['id']

    response = client.delete(f'/lessons/{lesson_id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 204

    get_response = client.get(f'/lessons/{lesson_id}')

    assert get_response.status_code == 404

def test_teacher_cannot_delete_other_teachers_lesson(client, db_session):
    owner = create_test_user(db_session, 'lesson_delete_owner@example.com', UserRole.TEACHER)
    other_teacher = create_test_user(db_session, 'lesson_delete_other@example.com', UserRole.TEACHER)

    owner_token = get_access_token(client, owner.email)
    other_token = get_access_token(client, other_teacher.email)

    course_id = create_course(client, owner_token)

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {owner_token}'}, json={'title': 'Protected Lesson', 'content': 'Another teacher must not delete this.'})

    assert create_response.status_code == 201

    lesson_id = create_response.json()['id']

    response = client.delete(f'/lessons/{lesson_id}', headers={'Authorization': f'Bearer {other_token}'})

    assert response.status_code == 403

def test_student_cannot_delete_lesson(client, db_session):
    teacher = create_test_user(db_session, 'protected_lesson_owner@example.com', UserRole.TEACHER)
    student = create_test_user(db_session, 'lesson_delete_student@example.com', UserRole.TEACHER)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Student Protected Lesson', 'content': 'Students must not delete this.'})

    assert create_response.status_code == 201

    lesson_id = create_response.json()['id']

    response = client.delete(f'/lessons/{lesson_id}', headers={'Authorization': f'Bearer {student_token}'})

    assert response.status_code == 403


def test_admin_can_delete_lesson(client, db_session):
    teacher = create_test_user(db_session, 'admin_can_delete_lesson@example.com', UserRole.TEACHER)
    admin = create_test_user(db_session, 'admin_can_do_everything@example.com', UserRole.ADMIN)

    teacher_token = get_access_token(client, teacher.email)
    admin_token = get_access_token(client, admin.email)

    course_id = create_course(client, teacher_token)

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Lesson For Admin To Delete', 'content': 'This lesson should be deleted by the admin.'})

    assert create_response.status_code == 201

    lesson_id = create_response.json()['id']

    response = client.delete(f'/lessons/{lesson_id}', headers={'Authorization': f'Bearer {admin_token}'})

    assert response.status_code == 204

    get_response = client.get(f'/lessons/{lesson_id}')

    assert get_response.status_code == 404


def test_student_can_complete_lesson(client, db_session):
    teacher = create_test_user(db_session, email='test_student_can_complete_lesson_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_can_complete_lesson@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'An ordinary course lesson', 'content': 'An ordinary content for a course lesson'})
    assert create_response.status_code == 201
    assert create_response.json()['title'] == 'An ordinary course lesson'
    data = create_response.json()

    lesson_id = data['id']

    student_course_enrollment_response = client.post(f'enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})


    assert student_course_enrollment_response.status_code == 201
    assert student_course_enrollment_response.json()['course_id'] == course_id
    assert student_course_enrollment_response.json()['student_id'] == student.id

    student_marks_lesson_complete_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_token}'})

    assert student_marks_lesson_complete_response.status_code == 201
    assert student_marks_lesson_complete_response.json()['lesson_id'] == lesson_id
    assert student_marks_lesson_complete_response.json()['student_id'] == student.id
    assert student_marks_lesson_complete_response.json()['completed_at'] is not None

def test_student_cannot_complete_lesson_without_enrollment(client, db_session):
    teacher = create_test_user(db_session, email='test_student_cannot_complete_lesson_without_enrollment_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_cannot_complete_lesson_without_enrollment@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Just a lesson', 'content': 'Just content of the lesson'})

    assert create_response.status_code == 201
    assert create_response.json()['title'] == 'Just a lesson'
    assert create_response.json()['course_id'] == published_course_id

    lesson_id = create_response.json()['id']

    student_marks_lesson_complete_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_token}'})

    assert student_marks_lesson_complete_response.status_code == 400


def test_student_cannot_complete_lesson_twice(client, db_session):
    teacher = create_test_user(db_session, email='test_student_cannot_complete_lesson_twice_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, email='this_student_cannot_complete_one_and_the_same_lesson_twice@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Just a lesson', 'content': 'Just content for the lesson'})

    assert create_response.status_code == 201
    assert create_response.json()['title'] == 'Just a lesson'
    assert create_response.json()['course_id'] == published_course_id

    lesson_id = create_response.json()['id']

    student_enrolls_in_course_response = client.post(f'/enrollments/courses/{published_course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert student_enrolls_in_course_response.status_code == 201
    assert student_enrolls_in_course_response.json()['course_id'] == published_course_id


    student_marks_lesson_complete_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_token}'})
    assert student_marks_lesson_complete_response.status_code == 201
    assert student_marks_lesson_complete_response.json()['lesson_id'] == lesson_id
    assert student_marks_lesson_complete_response.json()['student_id'] == student.id

    student_marks_same_lesson_complete_twice_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_token}'})
    assert student_marks_same_lesson_complete_twice_response.status_code == 400


def test_teacher_cannot_complete_lesson(client, db_session):
    teacher = create_test_user(db_session, email='test_teacher_cannot_complete_lesson_test_teacher@example.com', role=UserRole.TEACHER)
    teacher_token = get_access_token(client, teacher.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_lesson_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={"title": "A lesson that teacher cannot complete", 'content': 'this lesson should not completed bt the teacher'})
    assert create_lesson_response.status_code == 201
    assert create_lesson_response.json()['title'] == 'A lesson that teacher cannot complete'
    assert create_lesson_response.json()['course_id'] == published_course_id

    lesson_id = create_lesson_response.json()['id']

    teacher_cannot_enroll_in_course_response = client.post(f'/enrollments/courses/{published_course_id}/enroll', headers={'Authorization': f'Bearer {teacher_token}'})


    assert teacher_cannot_enroll_in_course_response.status_code == 403

    teacher_cannot_complete_lesson_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {teacher_token}'})
    assert teacher_cannot_complete_lesson_response.status_code == 403


def test_unauthenticated_user_cannot_complete_lesson(client, db_session):

    teacher = create_test_user(db_session, email='test_unauthenticated_user_cannot_complete_lesson_test_teacher@example.com', role=UserRole.TEACHER)
    teacher_token = get_access_token(client, teacher.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_lesson_response = client.post(f'/courses/{course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A lesson that unauthenticated user cannot complete', 'content': 'This lesson should not be completed by the unauthenticated user'})

    assert create_lesson_response.status_code == 201
    assert create_lesson_response.json()['title'] == 'A lesson that unauthenticated user cannot complete'
    assert create_lesson_response.json()['course_id'] == published_course_id

    lesson_id = create_lesson_response.json()['id']



    unauthenticated_user_cannot_complete_lesson_response = client.post(f'/lessons/{lesson_id}/complete')

    assert unauthenticated_user_cannot_complete_lesson_response.status_code == 401


def test_student_cannot_complete_missing_lesson(client, db_session):

    teacher = create_test_user(db_session, 'test_student_cannot_complete_missing_lesson_test_teacher@example.com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'this_student_cannot_complete_missing_lesson@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    student_course_enrollment_response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})

    assert student_course_enrollment_response.status_code == 201
    assert student_course_enrollment_response.json()['course_id'] == published_course_id

    student_attempt_to_complete_missing_lesson_response = client.post('lessons/999999/complete', headers={'Authorization': f'Bearer {student_token}'})

    assert student_attempt_to_complete_missing_lesson_response.status_code == 400


def test_student_can_get_own_progress(client, db_session):

    teacher = create_test_user(db_session, 'test_list_student_progress_test_teacher@example,com', role=UserRole.TEACHER)
    student = create_test_user(db_session, 'this_student_can_view_his_own_lesson_progress@example.com', role=UserRole.STUDENT)


    teacher_token = get_access_token(client, teacher.email)
    student_token = get_access_token(client, student.email)


    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})

    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_lesson_one_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A lesson that can be viewed by the student who enrolled to its own course', 'content': 'This lesson\'s progress should be viewed by the student who enrolled ro its course'})
    assert create_lesson_one_response.status_code == 201
    assert create_lesson_one_response.json()['title'] == 'A lesson that can be viewed by the student who enrolled to its own course'
    assert create_lesson_one_response.json()['course_id'] == published_course_id

    lesson_one_id = create_lesson_one_response.json()['id']

    create_lesson_two_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'A lesson that can be also viewed by the student who enrolled to its own course', 'content': 'This lesson\'s progress should also be viewed by the student who enrolled to is course'})
    assert create_lesson_two_response.status_code == 201
    assert create_lesson_two_response.json()['title'] == 'A lesson that can be also viewed by the student who enrolled to its own course'
    assert create_lesson_two_response.json()['course_id'] == published_course_id

    lesson_two_id = create_lesson_two_response.json()['id']

    student_course_enrollment_response = client.post(f'/enrollments/courses/{course_id}/enroll', headers={'Authorization': f'Bearer {student_token}'})
    assert student_course_enrollment_response.status_code == 201
    assert student_course_enrollment_response.json()['course_id'] == published_course_id

    student_marks_lesson_one_complete_response = client.post(f'/lessons/{lesson_one_id}/complete', headers={'Authorization': f'Bearer {student_token}'})
    assert student_marks_lesson_one_complete_response.status_code == 201
    assert student_marks_lesson_one_complete_response.json()['id'] == lesson_one_id
    assert student_marks_lesson_one_complete_response.json()['student_id'] == student.id
    assert student_marks_lesson_one_complete_response.json()['completed_at'] is not None

    student_marks_lesson_two_complete_response = client.post(f'/lessons/{lesson_two_id}/complete', headers={'Authorization': f'Bearer {student_token}'})
    assert student_marks_lesson_two_complete_response.status_code == 201
    assert student_marks_lesson_two_complete_response.json()['id'] == lesson_two_id
    assert student_marks_lesson_two_complete_response.json()['student_id'] == student.id
    assert student_marks_lesson_two_complete_response.json()['completed_at'] is not None


    student_gets_his_own_lesson_progress_response = client.get('/lessons/progress/me', headers={'Authorization': f'Bearer {student_token}'})

    assert student_gets_his_own_lesson_progress_response.status_code == 200
    assert student_gets_his_own_lesson_progress_response.json()[0]['lesson_id'] == lesson_one_id
    assert student_gets_his_own_lesson_progress_response.json()[0]['student_id'] == student.id
    assert student_gets_his_own_lesson_progress_response.json()[0]['completed_at'] is not None

    assert student_gets_his_own_lesson_progress_response.json()[1]['lesson_id'] == lesson_two_id
    assert student_gets_his_own_lesson_progress_response.json()[1]['student_id'] == student.id
    assert student_gets_his_own_lesson_progress_response.json()[1]['completed_at'] is not None

def test_student_only_sees_own_progress(client, db_session):
    teacher = create_test_user(db_session, 'test_student_only_sees_own_progress_test_teacher@example.com', role=UserRole.TEACHER)
    student_one = create_test_user(db_session, 'test_student_one_only_sess_his_own_lesson_progress@example.com', role=UserRole.STUDENT)
    student_two = create_test_user(db_session, 'test_student_two_only_sees_his_own_lesson_progress@example.com', role=UserRole.STUDENT)

    teacher_token = get_access_token(client, teacher.email)
    student_one_token = get_access_token(client, student_one.email)
    student_two_token = get_access_token(client, student_two.email)

    course_id = create_course(client, teacher_token)

    publish_course_response = client.post(f'/courses/{course_id}/publish', headers={'Authorization': f'Bearer {teacher_token}'})
    assert publish_course_response.status_code == 200
    assert publish_course_response.json()['id'] == course_id

    published_course_id = publish_course_response.json()['id']

    create_lesson_response = client.post(f'/courses/{published_course_id}/lessons', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Any lesson', 'content': 'Any lessons\'s content'})

    assert create_lesson_response.status_code == 201
    assert create_lesson_response.json()['title'] == 'Any lesson'
    assert create_lesson_response.json()['course_id'] == published_course_id

    lesson_id = create_lesson_response.json()['id']


    student_one_course_enrollment_response = client.post(f'/enrollments/courses/{published_course_id}/enroll', headers={'Authorization': f'Bearer {student_one_token}'})
    assert student_one_course_enrollment_response.status_code == 201
    assert student_one_course_enrollment_response.json()['course_id'] == published_course_id

    student_two_course_enrollment_response = client.post(f'/enrollments/courses/{published_course_id}/enroll', headers={'Authorization': f'Bearer {student_two_token}'})
    assert student_two_course_enrollment_response.status_code == 201
    assert student_two_course_enrollment_response.json()['course_id'] == published_course_id

    student_one_marks_lesson_complete_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_one_token}'})
    assert student_one_marks_lesson_complete_response.status_code == 201
    assert student_one_marks_lesson_complete_response.json()['lesson_id'] == lesson_id

    student_two_marks_lesson_complete_response = client.post(f'/lessons/{lesson_id}/complete', headers={'Authorization': f'Bearer {student_two_token}'})
    assert student_two_marks_lesson_complete_response.status_code == 201
    assert student_two_marks_lesson_complete_response.json()['lesson_id'] == lesson_id

    student_one_can_see_only_his_own_progress_response = client.get('lessons/progress/me', headers={'Authorization': f'Bearer {student_one_token}'})
    assert student_one_can_see_only_his_own_progress_response.status_code == 200
    assert student_one_can_see_only_his_own_progress_response.json()[0]['lesson_id'] == lesson_id
    assert student_one_can_see_only_his_own_progress_response.json()[0]['student_id'] == student_one.id

    student_two_can_see_only_his_own_progress_response = client.get('/lessons/progress/me', headers={'Authorization': f'Bearer {student_two_token}'})
    assert student_two_can_see_only_his_own_progress_response.status_code == 200
    assert student_two_can_see_only_his_own_progress_response.json()[0]['lesson_id'] == lesson_id
    assert student_two_can_see_only_his_own_progress_response.json()[0]['student_id'] != student_one.id
    assert student_two_can_see_only_his_own_progress_response.json()[0]['student_id'] == student_two.id
    assert student_two_can_see_only_his_own_progress_response.json()[0]['completed_at'] is not None


def test_teacher_cannot_get_my_progress(client, db_session):
    teacher = create_test_user(db_session, 'test_teacher_cannot_get_my_progress_test_teacher@example.com', role=UserRole.TEACHER)

    teacher_token = get_access_token(client, teacher.email)

    teachers_failed_attempt_to_get_students_lesson_progress_response = client.get('lessons/progress/me', headers={'Authorization': f'Bearer {teacher_token}'})
    assert teachers_failed_attempt_to_get_students_lesson_progress_response.status_code == 403

def test_unauthenticated_user_cannot_get_my_progress(client):

    unauthenticated_users_failed_attempt_to_get_students_lesson_progress_response = client.get('lessons/progress/me')
    assert unauthenticated_users_failed_attempt_to_get_students_lesson_progress_response.status_code == 401




































