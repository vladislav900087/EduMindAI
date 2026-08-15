from backend.app.models.user import User, UserRole
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








