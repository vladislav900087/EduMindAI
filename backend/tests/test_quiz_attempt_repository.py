from backend.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.user_repository import UserRepository

from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.quiz import Quiz
from backend.app.models.quiz_attempt import QuizAttempt

from backend.app.core.security import hash_password
from datetime import datetime
import uuid

def create_test_teacher_course_and_quiz(db_session):

    uid = uuid.uuid4().hex[:8]

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    quiz_repository = QuizRepository(db_session)

    user = User(email=f'test_user_{uid}@example.com', hashed_password=hash_password('Password123'), full_name=f'Test User {uid}', role=UserRole.TEACHER)
    user = user_repository.create(user)

    if user.role == UserRole.STUDENT:
        return None

    course = Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=user.id)

    course = course_repository.create(course)
    course = course_service.publish_course(course.id)


    quiz = Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id)
    quiz = quiz_repository.create(quiz)

    return user, course, quiz

def create_test_user(db_session, role: UserRole):
    uid = uuid.uuid4().hex[:8]

    user_repository = UserRepository(db_session)

    user = user_repository.create(User(email=f'test_user_{uid}@example.com', hashed_password=hash_password('Password123'), full_name='Test User', role=role))

    return user

def test_create_attempt(db_session):
    teacher, course, quiz = create_test_teacher_course_and_quiz(db_session)

    student = create_test_user(db_session, role=UserRole.STUDENT)

    attempt_repository = QuizAttemptRepository(db_session)

    attempt = attempt_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz.id))

    assert attempt is not None
    assert attempt.student_id == student.id
    assert attempt.quiz_id == quiz.id
    assert attempt.score is None
    assert attempt.completed_at is None

def test_get_attempt_by_id(db_session):
    teacher, course, quiz = create_test_teacher_course_and_quiz(db_session)

    student = create_test_user(db_session, role=UserRole.STUDENT)

    attempt_repository = QuizAttemptRepository(db_session)

    attempt = attempt_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz.id))

    assert attempt is not None
    assert attempt.student_id == student.id
    assert attempt.quiz_id == quiz.id
    assert attempt.score is None
    assert attempt.completed_at is None

    retrieved_attempt = attempt_repository.get_by_id(attempt.id)

    assert retrieved_attempt is not None
    assert retrieved_attempt == attempt

def test_get_attempt_by_id_returns_none_for_missing_attempt(db_session):

    attempt_repository = QuizAttemptRepository(db_session)

    retrieved_none_for_missing_attempt = attempt_repository.get_by_id(999999)

    assert retrieved_none_for_missing_attempt is None

def test_list_attempts_by_student(db_session):
    teacher, course, quiz = create_test_teacher_course_and_quiz(db_session)

    assert course.teacher_id == teacher.id

    student_a = create_test_user(db_session, role=UserRole.STUDENT)
    student_b = create_test_user(db_session, role=UserRole.STUDENT)

    attempt_repository = QuizAttemptRepository(db_session)

    student_a_attempt_one = attempt_repository.create(QuizAttempt(student_id=student_a.id, quiz_id=quiz.id))
    student_a_attempt_two = attempt_repository.create(QuizAttempt(student_id=student_a.id, quiz_id=quiz.id))

    student_b_attempt_one = attempt_repository.create(QuizAttempt(student_id=student_b.id, quiz_id=quiz.id))
    student_b_attempt_two = attempt_repository.create(QuizAttempt(student_id=student_b.id, quiz_id=quiz.id))

    assert student_a_attempt_one.quiz_id == student_b_attempt_one.quiz_id
    assert student_a_attempt_two.student_id != student_b_attempt_two.student_id

    student_a_attempts = attempt_repository.list_by_student(student_a.id)
    student_b_attempts = attempt_repository.list_by_student(student_b.id)

    assert len(student_a_attempts) == len(student_b_attempts)


def test_list_attempts_by_quiz(db_session):
    teacher_a, course_a, quiz_a = create_test_teacher_course_and_quiz(db_session)
    teacher_b, course_b, quiz_b = create_test_teacher_course_and_quiz(db_session)

    assert course_a.teacher_id == teacher_a.id
    assert course_b.teacher_id == teacher_b.id


    student = create_test_user(db_session, role=UserRole.STUDENT)

    attempts_repository = QuizAttemptRepository(db_session)


    quiz_a_attempt_one = attempts_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz_a.id))
    quiz_a_attempt_two = attempts_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz_a.id))

    quiz_b_attempt_one = attempts_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz_b.id))

    quiz_a_attempts = attempts_repository.list_by_quiz(quiz_a.id)
    quiz_b_attempts = attempts_repository.list_by_quiz(quiz_b.id)

    assert len(quiz_a_attempts) != len(quiz_b_attempts)
    assert quiz_a_attempts[1] == quiz_a_attempt_one
    assert quiz_a_attempts[0] == quiz_a_attempt_two
    assert quiz_b_attempts[0] == quiz_b_attempt_one

def test_update_attempt(db_session):
    teacher, course, quiz = create_test_teacher_course_and_quiz(db_session)

    assert course.teacher_id == teacher.id

    student = create_test_user(db_session, role=UserRole.STUDENT)

    attempts_repository = QuizAttemptRepository(db_session)

    attempt = attempts_repository.create(QuizAttempt(student_id=student.id, quiz_id=quiz.id))

    attempt.score = 80.0
    attempt.completed_at = datetime.now()

    updated_attempt = attempts_repository.update(attempt)

    assert updated_attempt.score == 80.0
    assert updated_attempt.completed_at is not None









    







