from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.quiz import Quiz
from backend.app.schemas.quiz_question import QuizOptionCreate
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.core.security import hash_password
import uuid
import random

def create_test_user_and_get_token(db_session, client,  role: UserRole):
    uid = uuid.uuid4().hex[:8]

    user_repository = UserRepository(db_session)


    user = User(email=f'test_user_{uid}@example.com', full_name='Test User', role=role, hashed_password=hash_password('SuperSecretPassword123!'))

    user = user_repository.create(user)

    response = client.post('/auth/login', data={'username': user.email, 'password': 'SuperSecretPassword123!'})

    assert response.status_code == 200

    access_token = response.json()['access_token']

    return user, access_token

def create_test_course_and_quiz(db_session, user: User):

    uid = uuid.uuid4().hex[:8]

    if user.role == UserRole.STUDENT:
        return None

    course_repository = CourseRepository(db_session)

    course_service = CourseService(course_repository)

    quiz_repository = QuizRepository(db_session)

    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Description', teacher_id=user.id))
    course = course_service.publish_course(course.id)

    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Description', course_id=course.id))

    return course, quiz

def create_test_options():
    options = []
    for i in range(3):
        option = {'option_text': f'Option {i + 1}', 'is_correct': False}
        options.append(option)


    options[random.randint(0, len(options) -1)]['is_correct'] = True

    return options

def test_teacher_can_create_question_for_own_quiz(db_session, client):
    teacher, teacher_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    uid = uuid.uuid4().hex[:8]

    options = [{'option_text': 'Option A', 'is_correct': True}, {"option_text": 'Option B', 'is_correct': False}, {'option_text': 'Option C', 'is_correct': False}]

    response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {teacher_token}'}, json={'question_text': f'Question Text {uid}?', 'options': options})

    assert response.status_code == 201


def test_admin_can_create_question(db_session, client):
    admin, admin_token = create_test_user_and_get_token(db_session, client, UserRole.ADMIN)
    course, quiz = create_test_course_and_quiz(db_session, admin)

    uid = uuid.uuid4().hex[:8]

    options = [{'option_text': 'Option One', 'is_correct': False}, {'option_text': 'Option Two', 'is_correct': True}, {'option_text': 'Option Three', 'is_correct': False}]

    response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {admin_token}'}, json={'question_text': f'Question Text {uid}?', 'options': options})

    assert response.status_code == 201

def test_teacher_cannot_create_question_for_another_teacher_quiz(db_session, client):
    teacher_a, teacher_a_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    teacher_b, teacher_b_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)

    course, quiz = create_test_course_and_quiz(db_session, teacher_a)

    uid = uuid.uuid4().hex[:8]

    options = []
    for i in range(3):
        option = {'option_text': f'Option {i + 1}', 'is_correct': False}
        options.append(option)

    options[0]['is_correct'] = True


    teacher_a_create_question_response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {teacher_a_token}'}, json={'question_text': f'Question Text {uid}?', 'options': options})

    assert teacher_a_create_question_response.status_code == 201

    teacher_b_create_question_response = client.post(f'/quizzes/{quiz.id}/questions', headers={"Authorization": f'Bearer {teacher_b_token}'}, json={'question_text': f'Invalid Question Text?', 'options': options})

    assert teacher_b_create_question_response.status_code == 403

def test_create_question_with_no_correct_option(db_session, client):
    teacher, teacher_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    options = create_test_options()

    for option in options:
        if option['is_correct']:
            option['is_correct'] = False

    response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {teacher_token}'}, json={'question_text': 'Some Question Text', 'options': options})

    assert response.status_code == 400

def test_create_question_with_multiple_correct_options(db_session, client):
    teacher, teacher_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    options = create_test_options()

    for option in options:
        if not option['is_correct']:
            option['is_correct'] = True

    options[random.randint(0, len(options) - 1)]['is_correct'] = False

    response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {teacher_token}'}, json={'question_text': 'A question with two correct options. INVALID!', 'options': options})
    assert response.status_code == 400

def test_create_question_with_one_option(db_session, client):

    teacher, teacher_token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    options = create_test_options()

    del options[2]
    del options[1]

    assert len(options) == 1

    response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {teacher_token}'}, json={'question_text': 'A Question with only one option. INVALID!', 'options': options})

    assert response.status_code == 400

def test_list_quiz_questions(db_session, client):
    teacher, token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    options = create_test_options()

    first_create_response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {token}'}, json={'question_text': f'Question Text {random.randint(0, 1000)}', 'options': options})
    assert first_create_response.status_code == 201
    second_create_response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {token}'}, json={'question_text': f'Question Text {random.randint(0, 1000)}', 'options': options})
    assert second_create_response.status_code == 201

    list_quiz_questions_response = client.get(f'/quizzes/{quiz.id}/questions')
    print(list_quiz_questions_response.status_code)
    print(list_quiz_questions_response.json())


def test_get_question(db_session, client):
    teacher, token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    options = create_test_options()

    create_response = client.post(f'/quizzes/{quiz.id}/questions', headers={'Authorization': f'Bearer {token}'}, json={'question_text': f'Quest Text {random.randint(0, 1000)}?', 'options': options})

    assert create_response.status_code == 201
    question_id = create_response.json()['id']

    retrieved_question_response = client.get(f'/questions/{question_id}')

    assert retrieved_question_response.status_code == 200
    assert retrieved_question_response.json()['id'] == question_id

def test_get_missing_question(client):

    response = client.get('questions/999999')

    assert response.status_code == 404

def test_unauthenticated_user_cannot_create_question(client, db_session):

    teacher, token = create_test_user_and_get_token(db_session, client, UserRole.TEACHER)
    course, quiz = create_test_course_and_quiz(db_session, teacher)

    response = client.post(f'/quizzes/{quiz.id}/questions')

    assert response.status_code == 401



















