from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository

from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.quiz import Quiz
from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption

from backend.app.core.security import hash_password
from typing import Optional
import uuid



def create_test_authenticated_user(db_session, client, role: UserRole) -> str:
    user_repository = UserRepository(db_session)
    uid = uuid.uuid4().hex[:8]
    default_password = 'SuperSecretPassword123!'

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password(default_password), role=role, full_name='Test User'))

    user_login_response = client.post('/auth/login', data={'username': user.email, 'password': default_password})

    assert user_login_response.status_code == 200

    user_token = user_login_response.json()['access_token']

    return user_token

def create_test_environment(db_session, client, return_question_id: Optional[bool] = False, return_selected_option_id: Optional[bool] = False):
    uid = uuid.uuid4().hex[:8]

    default_password = 'SuperSecretPassword123!'

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    enrollment_repository = CourseEnrollmentRepository(db_session)
    enrollment_service = CourseEnrollmentService(course_repository=course_repository, enrollment_repository=enrollment_repository)
    quiz_repository = QuizRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)

    teacher = user_repository.create(User(email=f'test_teacher_{uid}@example.com', hashed_password=hash_password(default_password), role=UserRole.TEACHER, full_name='Test Teacher'))
    student = user_repository.create(User(email=f'test_student_{uid}@example.com', hashed_password=hash_password(default_password), role=UserRole.STUDENT, full_name='Test Student'))

    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    course = course_service.publish_course(course_id=course.id)

    enrollment_service.enroll(course_id=course.id, student_id=student.id)

    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))

    question = question_repository.create_question(QuizQuestion(question_text=f'Test Quiz Question Text {uid}', quiz_id=quiz.id))

    question_options = []
    created_options = []

    for i in range(3):
        option = QuizOption(option_text=f'Test Quiz Option Number {i}', question_id=question.id, is_correct=False)
        question_options.append(option)

    question_options[0].is_correct = True


    for option in question_options:
        question_repository.create_option(option)
        created_options.append(option)

    student_login_response = client.post('/auth/login', data={'username': student.email, 'password': default_password})

    assert student_login_response.status_code == 200

    student_token = student_login_response.json()['access_token']

    if return_question_id == True and return_selected_option_id == False:
        return student_token, quiz, question.id

    if return_selected_option_id == True and return_question_id == False:
        return student_token, quiz, created_options[0].id

    if return_question_id == True and return_selected_option_id == True:
        return student_token, quiz, question.id, created_options[0].id

    else:

        return student_token, quiz


def create_test_environment_without_enrollment(db_session, client):
    uid = uuid.uuid4().hex[:8]

    default_password = 'SuperSecretPassword123!'

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    quiz_repository = QuizRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)

    teacher = user_repository.create(User(email=f'test_teacher_{uid}@example.com', hashed_password=hash_password(default_password), role=UserRole.TEACHER, full_name='Test Teacher'))
    student = user_repository.create(User(email=f'test_student_{uid}@example.com', hashed_password=hash_password(default_password), role=UserRole.STUDENT, full_name='Test Student'))

    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    course = course_service.publish_course(course_id=course.id)



    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))

    question = question_repository.create_question(QuizQuestion(question_text=f'Test Quiz Question Text {uid}', quiz_id=quiz.id))

    question_options = []

    for i in range(3):
        option = QuizOption(option_text=f'Test Quiz Option Number {i}', question_id=question.id, is_correct=False)
        question_options.append(option)

    question_options[0].is_correct = True

    for option in question_options:
        question_repository.create_option(option)

    student_login_response = client.post('/auth/login', data={'username': student.email, 'password': default_password})

    assert student_login_response.status_code == 200

    student_token = student_login_response.json()['access_token']

    return student_token, quiz


def test_student_can_start_quiz_attempt(db_session, client):

    student_token, quiz = create_test_environment(db_session, client)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 201

def test_correct_answers_are_not_exposed_when_starting_attempt(db_session, client):
    student_token, quiz = create_test_environment(db_session, client)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 201

    data = attempt_response.json()

    questions = data['questions']

    for question in questions:
        question_options = question['options']
        for option in question_options:
            assert 'is_correct' not in option

def test_non_student_cannot_start_quiz_attempt(db_session, client):
    student_token, quiz = create_test_environment(db_session, client)
    teacher_token = create_test_authenticated_user(db_session, client, role=UserRole.TEACHER)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {teacher_token}'})

    assert attempt_response.status_code == 403

def test_unenrolled_student_cannot_start_quiz_attempt(db_session, client):
    student_token, quiz = create_test_environment_without_enrollment(db_session, client)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 400

def test_student_can_submit_answer(db_session, client):
    student_token, quiz, question_id, selected_option_id = create_test_environment(db_session, client, return_question_id=True, return_selected_option_id=True)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 201

    data = attempt_response.json()

    attempt_id = data['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {student_token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 201

def test_student_cannot_submit_to_another_students_attempt(db_session, client):
    student_a_token, quiz, question_id, selected_option_id = create_test_environment(db_session, client, return_question_id=True, return_selected_option_id=True)
    student_b_token = create_test_authenticated_user(db_session, client, role=UserRole.STUDENT)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_a_token}'})
    assert attempt_response.status_code == 201

    data = attempt_response.json()

    attempt_id = data['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {student_b_token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 400

def test_student_cannot_submit_answer_twice(db_session, client):
    student_token, quiz, question_id, selected_option_id = create_test_environment(db_session, client, return_question_id=True, return_selected_option_id=True)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 201

    data = attempt_response.json()
    attempt_id = data['attempt']['id']

    submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {student_token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert submit_answer_response.status_code == 201

    second_submit_answer_response = client.post(f'/attempts/{attempt_id}/answers', headers={'Authorization': f'Bearer {student_token}'}, json={'question_id': question_id, 'selected_option_id': selected_option_id})

    assert second_submit_answer_response.status_code == 400

def test_student_can_get_own_attempt(db_session, client):
    student_token, quiz = create_test_environment(db_session, client)


    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_token}'})

    assert attempt_response.status_code == 201

    data = attempt_response.json()
    attempt_id = data['attempt']['id']

    get_attempt_response = client.get(f'/attempts/{attempt_id}', headers={'Authorization': f'Bearer {student_token}'})

    assert get_attempt_response.status_code == 200

def test_student_cannot_get_another_students_attempt(db_session, client):

    student_a_token, quiz = create_test_environment(db_session, client)
    student_b_token = create_test_authenticated_user(db_session, client, role=UserRole.STUDENT)

    attempt_response = client.post(f'/quizzes/{quiz.id}/attempts', headers={'Authorization': f'Bearer {student_a_token}'})

    assert attempt_response.status_code == 201

    data = attempt_response.json()
    attempt_id = data['attempt']['id']

    get_attempt_response = client.get(f'/attempts/{attempt_id}', headers={'Authorization': f'Bearer {student_b_token}'})

    assert get_attempt_response.status_code == 403

def test_unauthenticated_user_cannot_start_attempt(db_session, client):

    attempt_response = client.post(f'/quizzes/{999999}/attempts')

    assert attempt_response.status_code == 401


















