from backend.app.repositories.quiz_attempt_answer_repository import QuizAttemptAnswerRepository
from backend.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.user_repository import UserRepository

from backend.app.models.quiz_attempt_answer import QuizAttemptAnswer
from backend.app.models.quiz_attempt import QuizAttempt
from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption
from backend.app.models.quiz import Quiz
from backend.app.models.course import Course
from backend.app.models.user import User, UserRole

from backend.app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from typing import Optional
import pytest
import uuid

def create_test_environment(db_session, optional_variables_included: Optional[bool] = False):
    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    quiz_repository = QuizRepository(db_session)
    quiz_attempt_repository = QuizAttemptRepository(db_session)
    quiz_question_repository = QuizQuestionRepository(db_session)

    uid = uuid.uuid4().hex[:8]

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), role=UserRole.TEACHER, full_name='Test User'))
    student = user_repository.create(User(email=f'test_student_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), role=UserRole.STUDENT, full_name='Test Student'))
    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=user.id))
    course = course_service.publish_course(course_id=course.id)
    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))
    question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=quiz.id))
    option = quiz_question_repository.create_option(QuizOption(option_text=f'Option Text {uid}', question_id=question.id))
    quiz_attempt = quiz_attempt_repository.create(attempt=QuizAttempt(quiz_id=quiz.id, student_id=student.id))

    if optional_variables_included:
        return user, student, course, quiz, quiz_attempt, question, option

    return student, quiz_attempt, question, option

def test_create_attempt_answer(db_session):
    student, quiz_attempt, question, option = create_test_environment(db_session)

    answer_repository = QuizAttemptAnswerRepository(db_session)

    answer = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt.id, question_id=question.id, selected_option_id=option.id))

    assert answer is not None
    assert answer.attempt_id == quiz_attempt.id
    assert answer.question_id == question.id
    assert answer.selected_option_id == option.id

def test_get_attempt_answer_by_id(db_session):
    student, quiz_attempt, question, option = create_test_environment(db_session)

    answer_repository = QuizAttemptAnswerRepository(db_session)

    answer = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt.id, question_id=question.id, selected_option_id=option.id))

    assert answer is not None
    assert answer.attempt_id == quiz_attempt.id
    assert answer.question_id == question.id
    assert answer.selected_option_id == option.id

    retrieved_answer = answer_repository.get_by_id(answer_id=answer.id)

    assert retrieved_answer.id == answer.id

def test_get_attempt_answer_by_id_returns_none_for_missing_answer(db_session):

    answer_repository = QuizAttemptAnswerRepository(db_session)


    answer = answer_repository.get_by_id(answer_id=999999)

    assert answer is None


def test_get_answer_by_attempt_and_question(db_session):
    student, quiz_attempt, question, option = create_test_environment(db_session)

    answer_repository = QuizAttemptAnswerRepository(db_session)

    answer = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt.id, question_id=question.id, selected_option_id=option.id))

    assert answer is not None

    retrieved_answer = answer_repository.get_by_attempt_and_question(attempt_id=quiz_attempt.id, question_id=question.id)

    assert retrieved_answer is not None
    assert retrieved_answer.attempt_id == quiz_attempt.id
    assert retrieved_answer.question_id == question.id
    assert retrieved_answer.id == answer.id

def test_list_answers_by_attempt(db_session):

    student_one, quiz_attempt_one, question_one, option_for_question_one = create_test_environment(db_session)
    student_two, quiz_attempt_two, question_two, option_for_question_two = create_test_environment(db_session)

    answer_repository = QuizAttemptAnswerRepository(db_session)

    answer_for_question_one = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt_one.id, question_id=question_one.id, selected_option_id=option_for_question_one.id))
    answer_for_question_two = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt_one.id, question_id=question_two.id, selected_option_id=option_for_question_two.id))

    answer_for_question_one_second_attempt = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt_two.id, question_id=question_one.id, selected_option_id=option_for_question_one.id))


    assert answer_for_question_one is not None
    assert answer_for_question_two is not None
    assert answer_for_question_one_second_attempt is not None

    assert answer_for_question_one.attempt_id == quiz_attempt_one.id
    assert answer_for_question_two.attempt_id == quiz_attempt_one.id

    attempt_one_answers = answer_repository.list_by_attempt(attempt_id=quiz_attempt_one.id)
    attempt_two_answers = answer_repository.list_by_attempt(attempt_id=quiz_attempt_two.id)

    assert len(attempt_one_answers) == 2
    assert len(attempt_two_answers) == 1

def test_unique_attempt_question_constraint(db_session):

    student, quiz_attempt, question, option = create_test_environment(db_session)

    answer_repository = QuizAttemptAnswerRepository(db_session)

    answer = answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt.id, question_id=question.id, selected_option_id=option.id))

    assert answer is not None

    with pytest.raises(IntegrityError):
        answer_repository.create(QuizAttemptAnswer(attempt_id=quiz_attempt.id, question_id=question.id, selected_option_id=option.id))






