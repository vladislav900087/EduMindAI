from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository

from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.course_enrollment import CourseEnrollment
from backend.app.models.quiz import Quiz
from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption

from backend.app.core.security import hash_password
import uuid
from backend.tests.test_quiz_attempt_service import create_test_environment as cte, create_attempt_and_submit_answer




def login_user(client, email: str) -> str:
    login_response = client.post('/auth/login', data={'username': email, 'password': 'SuperSecretPassword123!'})

    assert login_response.status_code == 200

    return login_response.json()['access_token']

def complete_quiz_attempt(client, token: str,  attempt_id: int):

    response = client.post(f'/attempts/{attempt_id}/complete', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


def create_test_environment(db_session, client):
    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)
    quiz_repository = QuizRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)

    uid = uuid.uuid4().hex[:8]
    default_password = 'SuperSecretPassword123!'

    teacher = user_repository.create(User(email=f'test_teacher_{uid}@example.com', hashed_password=hash_password(default_password), full_name='Test Teacher', role=UserRole.TEACHER))
    student = user_repository.create(User(email=f'test_student_{uid}@example.com', hashed_password=hash_password(default_password), full_name='Test Student', role=UserRole.STUDENT))

    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    course = course_service.publish_course(course_id=course.id)

    enrollment_service.enroll(student_id=student.id, course_id=course.id)

    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))

    question = question_repository.create_question(QuizQuestion(question_text=f'Test Quiz Question {uid}', quiz_id=quiz.id))
    created_options = []

    for i in range(4):
        option = question_repository.create_option(QuizOption(option_text=f'Test Quiz Option {i}', question_id=question.id, is_correct=False))
        created_options.append(option)

    correct_option = created_options[0]

    correct_option.is_correct = True

    db_session.commit()
    db_session.refresh(correct_option)

    login_response = client.post('/auth/login', data={'username': student.email, 'password': default_password})
    assert login_response.status_code == 200

    token = login_response.json()['access_token']

    return token, quiz.id, question.id, correct_option.id

def create_test_user_and_login(db_session, client, role: UserRole):
    user_repository = UserRepository(db_session)

    uid = uuid.uuid4().hex[:8]

    default_password = 'SuperSecretPassword123!'

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password(default_password), full_name='Test User', role=role))

    login_response = client.post('/auth/login', data={"username": user.email, 'password': default_password})
    assert login_response.status_code == 200

    token = login_response.json()['access_token']

    return token


def test_student_can_complete_quiz_attempt(db_session, client):
    token, quiz_id, question_id, selected_option_id = create_test_environment(db_session, client)

    start_attempt_response = client.post(f'/quizzes/{quiz_id}/attempts', headers={'Authorization': f'Bearer {token}'})

    assert start_attempt_response.status_code == 201
    attempt_id = start_attempt_response.json()['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 201

    complete_attempt_response = client.post(f'/attempts/{attempt_id}/complete', headers={'Authorization': f'Bearer {token}'})

    assert complete_attempt_response.status_code == 200
    data = complete_attempt_response.json()
    assert data['score'] == 100.0
    assert data['completed_at'] is not None

def test_student_cannot_complete_another_students_attempt(db_session, client):
    token_a, quiz_id, question_id, selected_option_id = create_test_environment(db_session, client)
    token_b = create_test_user_and_login(db_session, client, UserRole.STUDENT)

    start_attempt_response = client.post(f'/quizzes/{quiz_id}/attempts', headers={'Authorization': f'Bearer {token_a}'})
    assert start_attempt_response.status_code == 201

    attempt_id = start_attempt_response.json()['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {token_a}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 201

    complete_attempt_response = client.post(f'/attempts/{attempt_id}/complete', headers={"Authorization": f'Bearer {token_b}'})
    assert complete_attempt_response.status_code == 400


def test_student_cannot_complete_attempt_twice(db_session, client):
    token, quiz_id, question_id, selected_option_id = create_test_environment(db_session, client)

    start_attempt_response = client.post(f'/quizzes/{quiz_id}/attempts', headers={'Authorization': f'Bearer {token}'})
    assert start_attempt_response.status_code == 201

    attempt_id = start_attempt_response.json()['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 201

    complete_attempt_response = client.post(f'/attempts/{attempt_id}/complete', headers={"Authorization": f'Bearer {token}'})

    assert complete_attempt_response.status_code == 200

    second_complete_attempt_response = client.post(f'/attempts/{attempt_id}/complete', headers={'Authorization': f'Bearer {token}'})

    assert second_complete_attempt_response.status_code == 400

def test_non_student_cannot_complete_attempt(db_session, client):

    teacher_token = create_test_user_and_login(db_session, client, UserRole.TEACHER)

    complete_attempt_response = client.post(f'/attempts/{999999}/complete', headers={'Authorization': f'Bearer {teacher_token}'})

    assert complete_attempt_response.status_code == 403

def unauthenticated_user_cannot_complete_attempt(client):

    complete_attempt_response = client.post('/attempts/999999/complete')

    assert complete_attempt_response.status_code == 401

def test_student_can_get_completed_attempt_history(db_session, client):
    student, quiz, qas = cte(db_session)
    attempt_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = login_user(client, student.email)

    complete_quiz_attempt(client=client, token=token, attempt_id=attempt_id)

    get_history_response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})

    assert get_history_response.status_code == 200

def test_list_completed_student_attempts_returns_empty_list(db_session, client):
    student, quiz, qas = cte(db_session)

    token = login_user(client, student.email)

    get_history_response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})

    assert get_history_response.status_code == 200
    assert get_history_response.json() == []

def test_student_history_excludes_uncompleted_attempts(db_session, client):
    student, quiz, qas = cte(db_session)

    attempt_one_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)
    attempt_two_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)
    attempt_three_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = login_user(client, student.email)


    complete_quiz_attempt(client=client, token=token, attempt_id=attempt_one_id)
    complete_quiz_attempt(client=client, token=token, attempt_id=attempt_two_id)

    first_response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})
    assert first_response.status_code == 200
    assert len(first_response.json()) == 2

    complete_quiz_attempt(client=client, token=token, attempt_id=attempt_three_id)

    second_response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})

    assert second_response.status_code == 200
    assert len(second_response.json()) == 3

def test_non_student_cannot_get_quiz_history(db_session, client):
    token = create_test_user_and_login(db_session, client, UserRole.TEACHER)

    response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403

def test_unauthenticated_user_cannot_get_quiz_history(client):

    response = client.get('/attempts/me')

    assert response.status_code == 401

def test_student_cannot_see_correct_answers_in_attempt_history(db_session, client):
    student, quiz, qas = cte(db_session)
    attempt_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = login_user(client, student.email)

    complete_quiz_attempt(client=client, token=token, attempt_id=attempt_id)

    response = client.get('/attempts/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert 'is_correct' not in response.json()[0]


def test_teacher_can_view_attempts_for_own_quiz(db_session, client):
    teacher, student, quiz, qas = cte(db_session, include_teacher=True)
    attempt_one_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)
    attempt_two_id = create_attempt_and_submit_answer(db_session, student, quiz, qas)

    student_token = login_user(client, student.email)
    teacher_token = login_user(client, teacher.email)

    complete_quiz_attempt(client=client, token=student_token, attempt_id=attempt_one_id)
    complete_quiz_attempt(client=client, token=student_token, attempt_id=attempt_two_id)

    response = client.get(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {teacher_token}'})

    assert response.status_code == 200

def test_admin_can_view_quiz_attempts(db_session, client):
    student, quiz, qas = cte(db_session)

    create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = create_test_user_and_login(db_session, client, UserRole.ADMIN)

    response = client.get(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


def test_teacher_cannot_view_another_teachers_attempts(db_session, client):
    student, quiz, qas = cte(db_session)
    create_attempt_and_submit_answer(db_session, student, quiz, qas)

    teacher_b_token = create_test_user_and_login(db_session, client, UserRole.TEACHER)

    response = client.get(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {teacher_b_token}'})

    assert response.status_code == 403

def test_student_cannot_view_quiz_attempts(db_session, client):
    student, quiz, qas = cte(db_session)
    create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = login_user(client, student.email)

    response = client.get(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403

def test_teacher_can_view_uncompleted_quiz_attempts(db_session, client):
    teacher, student, quiz, qas = cte(db_session, include_teacher=True)
    create_attempt_and_submit_answer(db_session, student, quiz, qas)

    token = login_user(client, teacher.email)

    response = client.get(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()[0]['score'] is None
    assert response.json()[0]['completed_at'] is None
    assert 'is_correct' not in response.json()[0]

def test_unauthenticated_user_cannot_view_quiz_attempts(client):

    response = client.get('/quizzes/999999/attempts')

    assert response.status_code == 401





























