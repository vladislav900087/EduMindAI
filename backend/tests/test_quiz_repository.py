

from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService

from backend.app.models.quiz import Quiz
from backend.app.models.user import User, UserRole
from backend.app.models.course import Course, CourseStatus
import random

from backend.app.core.security import hash_password


def create_test_user(db_session, email: str, role: UserRole) -> User:
    user = User(email=email, role=role, full_name='Test User', hashed_password=hash_password('SuperSecretPassword123!'))

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def create_and_publish_test_course(db_session):
    teacher = create_test_user(db_session, f'test_teacher{random.randint(1, 1000)}@example.com', role=UserRole.TEACHER)

    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)

    created_course = course_repository.create(Course(title=f'Test Course {random.randint(1, 1000)}', description='Description for Test Course', teacher_id=teacher.id))


    published_course = course_service.publish_course(created_course.id)

    return published_course, teacher


def test_create_quiz(db_session):
    published_course, teacher = create_and_publish_test_course(db_session)

    assert published_course is not None
    assert teacher is not None

    assert published_course.teacher_id == teacher.id
    assert published_course.status == CourseStatus.PUBLISHED

    quiz_repository = QuizRepository(db_session)

    quiz = quiz_repository.create(Quiz(title=f'Random quiz {random.randint(1, 1000)}', description='Description for Random Quiz', course_id=published_course.id))

    assert quiz is not None
    assert quiz.course_id == published_course.id
    assert quiz.description == 'Description for Random Quiz'

def test_get_quiz_by_id(db_session):
    published_course, teacher = create_and_publish_test_course(db_session)

    assert published_course is not None
    assert teacher is not None
    assert published_course.teacher_id == teacher.id
    assert published_course.status == CourseStatus.PUBLISHED

    quiz_repository = QuizRepository(db_session)

    created_quiz = quiz_repository.create(Quiz(title=f'Random Quiz {random.randint(1, 1000)}', description='Description for Random Quiz', course_id=published_course.id))

    assert created_quiz is not None
    assert created_quiz.course_id == published_course.id
    assert created_quiz.description == 'Description for Random Quiz'

    fetched_quiz = quiz_repository.get_by_id(created_quiz.id)

    assert fetched_quiz is not None
    assert fetched_quiz.course_id == published_course.id
    assert fetched_quiz.description == 'Description for Random Quiz'
    assert fetched_quiz.id == created_quiz.id


def test_get_quiz_by_id_returns_none_for_missing_quiz(db_session):

    quiz_repository = QuizRepository(db_session)

    fetched_none_quiz = quiz_repository.get_by_id(999999)

    assert fetched_none_quiz is None

def test_list_quizzes_by_course(db_session):
    published_course_a, teacher_a = create_and_publish_test_course(db_session)
    published_course_b, teacher_b = create_and_publish_test_course(db_session)

    assert published_course_a is not None
    assert teacher_a is not None
    assert published_course_a.teacher_id == teacher_a.id
    assert published_course_a.status == CourseStatus.PUBLISHED


    assert published_course_b is not None
    assert teacher_b is not None
    assert published_course_b.teacher_id == teacher_b.id
    assert published_course_b.status == CourseStatus.PUBLISHED

    quiz_repository = QuizRepository(db_session)

    created_course_a_quiz_one = quiz_repository.create(Quiz(title=f'Random Quiz {random.randint(1, 1000)}', description='Description for Random Quiz', course_id=published_course_a.id))
    created_course_a_quiz_two = quiz_repository.create(Quiz(title=f'Random Quiz {random.randint(1, 1000)}', description='Description for Random Quiz', course_id=published_course_a.id))

    created_course_b_quiz_one = quiz_repository.create(Quiz(title=f'Random Quiz {random.randint(1, 1000)},', description='Description for Random Quiz', course_id=published_course_b.id))
    created_course_b_quiz_two = quiz_repository.create(Quiz(title=f'Random Quiz {random.randint(1, 1000)}', description='Description for Random Quiz', course_id=published_course_b.id))

    assert created_course_a_quiz_one is not None
    assert created_course_a_quiz_one.course_id == published_course_a.id

    assert created_course_a_quiz_two is not None
    assert created_course_a_quiz_two.course_id == published_course_a.id

    assert created_course_b_quiz_one is not None
    assert created_course_b_quiz_one.course_id == published_course_b.id

    assert created_course_b_quiz_two is not None
    assert created_course_b_quiz_two.course_id == published_course_b.id

    listed_course_a_quizzes = quiz_repository.list_by_course(course_id=published_course_a.id)
    listed_course_b_quizzes = quiz_repository.list_by_course(course_id=published_course_b.id)

    assert len(listed_course_a_quizzes) == 2
    assert len(listed_course_b_quizzes) == 2
    assert len(listed_course_a_quizzes) == len(listed_course_b_quizzes)

    assert listed_course_a_quizzes[0].course_id == published_course_a.id
    assert listed_course_b_quizzes[0].course_id == published_course_b.id







