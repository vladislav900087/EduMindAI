from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.services.quiz_service import QuizService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.services.quiz_service import QuizService
from backend.app.repositories.user_repository import UserRepository
from backend.app.models.user import User, UserRole
from backend.app.models.course import Course, CourseStatus
from backend.app.models.quiz import Quiz
from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption

import uuid
import random
from backend.app.core.security import hash_password

def create_test_user_course_and_quiz(db_session, role: UserRole):
    uid = uuid.uuid4().hex[:8]
    user_repository = UserRepository(db=db_session)

    course_repository = CourseRepository(db=db_session)
    course_service = CourseService(repository=course_repository)

    quiz_repository = QuizRepository(db=db_session)


    user = User(email=f'test_user_{uid}@example.com', hashed_password=hash_password('StrongPassword123!'), full_name=f'Test User {uid}', role=role)

    created_user = user_repository.create(user)

    if created_user.role == UserRole.STUDENT:
        return None

    course = Course(title=f'Test Course {uid}', description=f'Test Course Description {uid}', teacher_id=created_user.id)
    created_course = course_repository.create(course)
    published_course = course_service.publish_course(created_course.id)

    quiz = Quiz(title=f'Test Quiz {uid}', description=f'Test Quiz Description {uid}', course_id=published_course.id)
    created_quiz = quiz_repository.create(quiz)

    return published_course, created_quiz, created_user


def test_create_question(db_session):

    published_course, created_quiz, created_user = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    uid = uuid.uuid4().hex[:8]

    assert published_course is not None
    assert created_quiz is not None
    assert created_user is not None

    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    quiz_question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz.id))

    assert quiz_question is not None
    assert quiz_question.quiz_id == created_quiz.id

def test_create_option(db_session):
    published_course, created_quiz, created_user = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    uid = uuid.uuid4().hex[:8]

    assert published_course is not None
    assert created_quiz is not None
    assert created_user is not None

    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz.id))
    assert question is not None
    assert question.quiz_id == created_quiz.id

    option = quiz_question_repository.create_option(QuizOption(option_text=f'Question Option Text {uid}', question_id=question.id))

    assert option is not None
    assert option.question_id == question.id


def test_get_question_by_id(db_session):
    published_course, created_quiz, created_user = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    uid = uuid.uuid4().hex[:8]

    assert published_course is not None
    assert created_quiz is not None
    assert created_user is not None

    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    created_question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}', quiz_id=created_quiz.id))

    assert created_question is not None
    assert created_question.quiz_id == created_quiz.id

    retrieved_question = quiz_question_repository.get_by_id(created_question.id)

    assert retrieved_question is not None
    assert retrieved_question.id == created_question.id
    assert retrieved_question.question_text == created_question.question_text
    assert retrieved_question.quiz_id == created_question.quiz_id


def test_get_question_by_id_returns_none_for_missing_question(db_session):
    question_repository = QuizQuestionRepository(db=db_session)

    none_instead_of_retrieved_question = question_repository.get_by_id(999999)

    assert none_instead_of_retrieved_question is None

def test_list_questions_by_quiz(db_session):
    published_course_a, created_quiz_a, created_user_a = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    published_course_b, created_quiz_b, created_user_b = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    uid = uuid.uuid4().hex[:8]

    assert published_course_a is not None
    assert created_quiz_a is not None
    assert created_user_a is not None

    assert published_course_a.teacher_id == created_user_a.id
    assert created_quiz_a.course_id == published_course_a.id

    assert published_course_a.status == CourseStatus.PUBLISHED

    assert published_course_b is not None
    assert created_quiz_b is not None
    assert created_user_b is not None

    assert published_course_b.teacher_id == created_user_b.id
    assert created_quiz_b.course_id == published_course_b.id

    assert published_course_b.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    quiz_a_question_one = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz_a.id))
    quiz_a_question_two = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz_a.id))

    assert quiz_a_question_one is not None
    assert quiz_a_question_one.quiz_id == created_quiz_a.id

    assert quiz_a_question_two is not None
    assert quiz_a_question_two.quiz_id == created_quiz_a.id

    quiz_b_question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz_b.id))

    assert quiz_b_question is not None
    assert quiz_b_question.quiz_id == created_quiz_b.id
    assert quiz_b_question.quiz_id != created_quiz_a.id

    quiz_a_questions = quiz_question_repository.list_by_quiz(created_quiz_a.id)
    quiz_b_questions = quiz_question_repository.list_by_quiz(created_quiz_b.id)

    assert len(quiz_a_questions) == 2
    assert len(quiz_b_questions) == 1

def test_list_options(db_session):
    published_course, created_quiz, created_user = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    uid = uuid.uuid4().hex[:8]

    assert published_course is not None
    assert created_quiz is not None
    assert created_user is not None

    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    question = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz.id))

    assert question is not None
    assert question.quiz_id == created_quiz.id

    option_one = quiz_question_repository.create_option(QuizOption(option_text=f'Option Text {random.randint(1, 1000)}', question_id=question.id))

    assert option_one is not None
    assert option_one.question_id == question.id

    option_two = quiz_question_repository.create_option(QuizOption(option_text=f'Option Text {random.randint(1, 1000)}', question_id=question.id))

    assert option_two is not None
    assert option_two.question_id == question.id

    option_three = quiz_question_repository.create_option(QuizOption(option_text=f'Option Text {random.randint(1, 1000)}', question_id=question.id))

    assert option_three is not None
    assert option_three.question_id == question.id

    question_options = quiz_question_repository.list_options(created_quiz.id)

    assert len(question_options) == 3
    assert question_options == question.options


def test_delete_question(db_session):
    published_course, created_quiz, created_user = create_test_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    uid = uuid.uuid4().hex[:8]

    assert published_course is not None
    assert created_quiz is not None
    assert created_user is not None

    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    quiz_question_repository = QuizQuestionRepository(db=db_session)

    question_to_delete = quiz_question_repository.create_question(QuizQuestion(question_text=f'Question Text {uid}?', quiz_id=created_quiz.id))

    assert question_to_delete is not None
    assert question_to_delete.quiz_id == created_quiz.id

    deleted_question = quiz_question_repository.delete(question_to_delete)

    assert deleted_question is None








