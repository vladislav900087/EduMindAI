from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.services.quiz_service import QuizService
from backend.app.schemas.quiz import QuizCreate

from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService


from backend.app.models.course import Course, CourseStatus
from backend.app.models.user import User, UserRole

from backend.app.core.security import hash_password

import pytest
import random
import uuid

def create_test_course(db_session):
    teacher = User(email=f'test_teacher_{random.randint(1, 1000)}', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Teacher', role=UserRole.TEACHER)

    db_session.add(teacher)
    db_session.commit()
    db_session.refresh(teacher)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)

    course = Course(title=f'Test Course {random.randint(1, 1000)}', description='Test Description', teacher_id=teacher.id)

    created_course = course_repository.create(course)

    published_course = course_service.publish_course(created_course.id)

    return published_course


def test_create_quiz(db_session):
    course = create_test_course(db_session)

    quiz_repository = QuizRepository(db_session)
    quiz_service = QuizService(quiz_repository)

    created_quiz = quiz_service.create_quiz(course_id=course.id, quiz_data=QuizCreate(title=f'Test Quiz {random.randint(1, 1000)}', description='Test Quiz Description'))
    assert created_quiz is not None
    assert created_quiz.course_id == course.id
    assert created_quiz.description == 'Test Quiz Description'

def test_get_quiz(db_session):
    course = create_test_course(db_session)

    quiz_repository = QuizRepository(db_session)
    quiz_service = QuizService(quiz_repository)

    created_quiz = quiz_service.create_quiz(course_id=course.id, quiz_data=QuizCreate(title=f'Test Quiz {random.randint(1, 1000)}', description='Test Quiz Description'))
    assert created_quiz is not None
    assert created_quiz.course_id == course.id
    assert created_quiz.description == 'Test Quiz Description'

    retrieved_quiz = quiz_service.get_quiz(created_quiz.id)

    assert retrieved_quiz is not None
    assert retrieved_quiz.id == created_quiz.id
    assert retrieved_quiz.title == created_quiz.title
    assert retrieved_quiz.description == created_quiz.description
    assert retrieved_quiz.course_id == created_quiz.course_id

def test_get_missing_quiz(db_session):
    quiz_repository = QuizRepository(db_session)
    quiz_service = QuizService(quiz_repository)

    with pytest.raises(ValueError, match='Quiz not found'):
        quiz_service.get_quiz(quiz_id=999999)

def test_list_course_quizzes(db_session):
    course_a = create_test_course(db_session)
    course_b = create_test_course(db_session)

    quiz_repository = QuizRepository(db_session)
    quiz_service = QuizService(quiz_repository)

    uid = uuid.uuid4().hex[:8]

    quiz_one = quiz_service.create_quiz(course_id=course_a.id, quiz_data=QuizCreate(title=f'Test Quiz {uid}', description='Test Quiz Description'))

    assert quiz_one is not None
    assert quiz_one.course_id == course_a.id

    quiz_two = quiz_service.create_quiz(course_id=course_a.id, quiz_data=QuizCreate(title=f'Test Quiz {uid}', description='Test Quiz Description'))

    assert quiz_two is not None
    assert quiz_two.course_id == course_a.id

    quiz_three = quiz_service.create_quiz(course_id=course_b.id, quiz_data=QuizCreate(title=f'Test Quiz {uid}', description='Test Quiz Description'))

    assert quiz_three is not None
    assert quiz_three.course_id == course_b.id

    course_a_quizzes = quiz_service.list_course_quizzes(course_id=course_a.id)
    course_b_quizzes = quiz_service.list_course_quizzes(course_id=course_b.id)

    assert len(course_a_quizzes) == 2
    assert len(course_b_quizzes) == 1
