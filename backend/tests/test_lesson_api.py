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
