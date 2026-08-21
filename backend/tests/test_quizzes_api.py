from backend.app.models.user import User, UserRole
from backend.app.models.course import Course, CourseStatus
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.core.security import hash_password
import uuid

def create_test_user(db_session, role: UserRole):
    uid = uuid.uuid4().hex[:8]
    user = User(email=f'test_user_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Teacher', role=role)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def get_token(client, email: str):

    response = client.post('/auth/login', data={'username': email, 'password': 'SuperSecretPassword123!'})

    token = response.json()['access_token']

    return token

def create_test_course(db_session, teacher: User):
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)

    uid = uuid.uuid4().hex[:8]

    created_course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    published_course = course_service.publish_course(created_course.id)

    return published_course



def test_teacher_can_create_quiz_for_own_course(db_session, client):
    teacher = create_test_user(db_session, role=UserRole.TEACHER)
    teacher_token = get_token(client, teacher.email)

    course = create_test_course(db_session, teacher)

    uid = uuid.uuid4().hex[:8]

    response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Quiz {uid}', 'description': 'Test Quiz Description'})

    assert response.status_code == 201
    assert response.json()['course_id'] == course.id

def test_student_cannot_create_quiz(db_session, client):
    teacher = create_test_user(db_session, role=UserRole.TEACHER)
    student = create_test_user(db_session, role=UserRole.STUDENT)


    student_token = get_token(client, student.email)

    course = create_test_course(db_session, teacher)

    assert course.status == CourseStatus.PUBLISHED

    student_tries_to_create_quiz_response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {student_token}'}, json={'title': 'Test Quiz', 'description': 'Test Quiz Description'})

    assert student_tries_to_create_quiz_response.status_code == 403

def test_teacher_cannot_create_quiz_for_another_teacher_course(db_session, client):
    teacher_a = create_test_user(db_session, role=UserRole.TEACHER)
    teacher_b = create_test_user(db_session, role=UserRole.TEACHER)

    teacher_b_token = get_token(client, teacher_b.email)

    course = create_test_course(db_session, teacher_a)

    assert course.status == CourseStatus.PUBLISHED
    assert course.teacher_id == teacher_a.id

    teacher_b_tries_to_create_quiz_for_teacher_a_course_response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_b_token}'}, json={'title': 'Test Quiz', 'description': 'Test Quiz Description'})

    assert teacher_b_tries_to_create_quiz_for_teacher_a_course_response.status_code == 403

def test_create_quiz_for_missing_course(db_session, client):
    teacher = create_test_user(db_session, role=UserRole.TEACHER)

    teacher_token = get_token(client, teacher.email)

    response = client.post('/courses/999999/quizzes', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': 'Test Quiz', 'description': 'Test Quiz Description'})

    assert response.status_code == 404

def test_list_course_quizzes(db_session, client):
    teacher = create_test_user(db_session, role=UserRole.TEACHER)

    teacher_token = get_token(client, teacher.email)

    uid_1 = uuid.uuid4().hex[:8]
    uid_2 = uuid.uuid4().hex[:8]

    course = create_test_course(db_session, teacher)

    assert course.status == CourseStatus.PUBLISHED
    assert course.teacher_id == teacher.id

    create_quiz_one_response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Quiz {uid_1}', 'description': 'Test Quiz Description'})
    assert create_quiz_one_response.status_code == 201
    assert create_quiz_one_response.json()['course_id'] == course.id

    create_quiz_two_response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Quiz {uid_2}', 'description': 'Test Quiz Description'})
    assert create_quiz_two_response.status_code == 201
    assert create_quiz_two_response.json()['course_id'] == course.id

    list_course_quizzes_response = client.get(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_token}'})

    assert list_course_quizzes_response.status_code == 200
    assert len(list_course_quizzes_response.json()) == 2
    assert list_course_quizzes_response.json()[0]['course_id'] == course.id
    assert list_course_quizzes_response.json()[1]['course_id'] == course.id


def test_get_quiz(db_session, client):
    teacher = create_test_user(db_session, role=UserRole.TEACHER)
    teacher_token = get_token(client, teacher.email)

    uid = uuid.uuid4().hex[:8]
    course = create_test_course(db_session, teacher)

    assert course.status == CourseStatus.PUBLISHED
    assert course.teacher_id == teacher.id

    create_course_quiz_response = client.post(f'/courses/{course.id}/quizzes', headers={'Authorization': f'Bearer {teacher_token}'}, json={'title': f'Test Quiz {uid}', 'description': 'Test Quiz Description'})
    assert create_course_quiz_response.status_code == 201
    assert create_course_quiz_response.json()['course_id'] == course.id

    quiz_id = create_course_quiz_response.json()['id']

    retrieve_course_quiz_response = client.get(f'/quizzes/{quiz_id}')

    assert retrieve_course_quiz_response.status_code == 200
    assert retrieve_course_quiz_response.json()['id'] == quiz_id
    assert retrieve_course_quiz_response.json()['course_id'] == course.id

def test_get_missing_quiz(db_session, client):
    response = client.get('/quizzes/999999')

    assert response.status_code == 404

def test_unauthenticated_user_cannot_create_quiz(db_session, client):
    response = client.post('/courses/999999/quizzes')

    assert response.status_code == 401








