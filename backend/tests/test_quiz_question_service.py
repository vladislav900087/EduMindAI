from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.services.quiz_question_service import QuizQuestionService
from backend.app.schemas.quiz_question import QuizQuestionCreate, QuizOptionCreate

from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.models.quiz import Quiz


from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.models.course import Course, CourseStatus

from backend.app.repositories.user_repository import UserRepository
from backend.app.models.user import User, UserRole

from backend.app.core.security import hash_password
import pytest
import uuid


def create_user_course_and_quiz(db_session, role: UserRole):
    uid = uuid.uuid4().hex[:8]

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    quiz_repository = QuizRepository(db_session)

    user = User(email=f'test_user_{uid}@example.com', full_name=f'Test User {uid}', role=role, hashed_password=hash_password('SuperSecretPassword123!'))

    created_user = user_repository.create(user)

    if created_user.role == UserRole.STUDENT:
        return None

    course = Course(title=f'Test Course {uid}', description=f'Test Course Description {uid}', teacher_id=created_user.id)

    created_course = course_repository.create(course)
    published_course = course_service.publish_course(created_course.id)

    quiz = Quiz(title=f'Test Quiz {uid}', description=f'Test Quiz Description {uid}', course_id=published_course.id)

    created_quiz = quiz_repository.create(quiz)

    return created_user, published_course, created_quiz


def test_create_question(db_session):
    created_user, published_course, created_quiz = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    assert created_user is not None
    assert published_course is not None
    assert created_quiz is not None

    assert created_user.id == published_course.teacher_id
    assert published_course.id == created_quiz.course_id

    assert created_user.role == UserRole.TEACHER
    assert published_course.status == CourseStatus.PUBLISHED

    uid = uuid.uuid4().hex[:8]

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_one = QuizOptionCreate(option_text='Option One', is_correct=True)
    option_two = QuizOptionCreate(option_text='Option Two', is_correct=False)
    option_three = QuizOptionCreate(option_text='Option Three')

    option_data.append(option_one)
    option_data.append(option_two)
    option_data.append(option_three)

    assert len(option_data) == 3

    correct_options = [option for option in option_data if option.is_correct]
    assert len(correct_options) == 1


    question_data = QuizQuestionCreate(question_text=f'Question Text {uid}?', options=option_data)
    question = question_service.create_question(quiz_id=created_quiz.id, question_data=question_data)

    assert question is not None
    assert question.quiz_id == created_quiz.id
    assert len(question.options) == 3
    assert len([option for option in question.options if option.is_correct]) == 1


def test_create_question_requires_at_least_two_options(db_session):
    created_user, published_course, created_quiz = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    assert created_user is not None
    assert published_course is not None
    assert created_quiz is not None

    assert created_user.role == UserRole.TEACHER
    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    uid = uuid.uuid4().hex[:8]

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_one = QuizOptionCreate(option_text='Option One', is_correct=True)

    option_data.append(option_one)

    assert len(option_data) == 1

    question_data = QuizQuestionCreate(question_text=f'Question Text {uid}?', options=option_data)

    with pytest.raises(ValueError, match='A question must have at least 2 options'):
        question_service.create_question(quiz_id=created_quiz.id, question_data=question_data)


def test_create_question_requires_exactly_one_correct_option(db_session):
    created_user, published_course, created_quiz = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    assert created_user is not None
    assert published_course is not None
    assert created_quiz is not None

    assert created_user.role == UserRole.TEACHER
    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    uid = uuid.uuid4().hex[:8]

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_one = QuizOptionCreate(option_text='Option One', is_correct=False)
    option_two = QuizOptionCreate(option_text='Option Two', is_correct=False)
    option_three = QuizOptionCreate(option_text='Option Three', is_correct=False)

    option_data.append(option_one)
    option_data.append(option_two)
    option_data.append(option_three)

    correct_options = [option for option in option_data if option.is_correct]
    assert len(correct_options) == 0

    question_data = QuizQuestionCreate(question_text=f'Question Text {uid}?', options=option_data)

    with pytest.raises(ValueError, match='A question must have exactly 1 correct option'):
        question_service.create_question(quiz_id=created_quiz.id, question_data=question_data)



def test_create_question_for_missing_quiz(db_session):

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_one = QuizOptionCreate(option_text='Option One', is_correct=True)

    option_data.append(option_one)

    question_data = QuizQuestionCreate(question_text='Question for missing quiz', options=option_data)

    with pytest.raises(ValueError, match='Quiz not found'):
        question_service.create_question(quiz_id=999999, question_data=question_data)


def test_get_question(db_session):
    created_user, published_course, created_quiz = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    assert created_user is not None
    assert published_course is not None
    assert created_quiz is not None

    assert created_user.role == UserRole.TEACHER
    assert published_course.teacher_id == created_user.id
    assert created_quiz.course_id == published_course.id

    assert published_course.status == CourseStatus.PUBLISHED

    uid = uuid.uuid4().hex[:8]

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_one = QuizOptionCreate(option_text='Option One', is_correct=True)
    option_two = QuizOptionCreate(option_text='Option Two', is_correct=False)
    option_three = QuizOptionCreate(option_text='Option Three', is_correct=False)

    option_data.append(option_one)
    option_data.append(option_two)
    option_data.append(option_three)

    assert len(option_data) == 3

    assert len([option for option in option_data if option.is_correct]) == 1

    question_data = QuizQuestionCreate(question_text=f'Question Text {uid}?', options=option_data)

    created_question = question_service.create_question(quiz_id=created_quiz.id, question_data=question_data)

    assert created_question is not None
    assert created_question.quiz_id == created_quiz.id
    assert len(created_question.options) == 3
    assert len([option for option in created_question.options if option.is_correct]) == 1

    retrieved_question = question_service.get_question(created_question.id)

    assert retrieved_question is not None
    assert retrieved_question.id == created_question.id
    assert retrieved_question.quiz_id == created_question.quiz_id
    assert retrieved_question.question_text == created_question.question_text
    assert retrieved_question.options == created_question.options

def test_get_missing_question(db_session):


    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    with pytest.raises(ValueError, match='Question not found'):
        question_service.get_question(question_id=999999)

def test_list_quiz_questions(db_session):
    created_user_a, published_course_a, created_quiz_a = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)
    created_user_b, published_course_b, created_quiz_b = create_user_course_and_quiz(db_session, role=UserRole.TEACHER)

    assert created_user_a.id == published_course_a.teacher_id
    assert created_user_b.id == published_course_b.teacher_id

    question_repository = QuizQuestionRepository(db_session)
    quiz_repository = QuizRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    option_data = []

    option_a = QuizOptionCreate(option_text='Option A', is_correct=True)
    option_b = QuizOptionCreate(option_text='Option B', is_correct=False)
    option_c = QuizOptionCreate(option_text='Option C', is_correct=False)

    option_data.append(option_a)
    option_data.append(option_b)
    option_data.append(option_c)

    question_one_data_for_quiz_a = QuizQuestionCreate(question_text='Question 1', options=option_data)
    question_two_data_for_quiz_a = QuizQuestionCreate(question_text='Question 2', options=option_data)

    question_one_data_for_quiz_b = QuizQuestionCreate(question_text='Question 3', options=option_data)

    question_service.create_question(quiz_id=created_quiz_a.id, question_data=question_one_data_for_quiz_a)
    question_service.create_question(quiz_id=created_quiz_a.id, question_data=question_two_data_for_quiz_a)
    question_service.create_question(quiz_id=created_quiz_b.id, question_data=question_one_data_for_quiz_b)

    quiz_a_questions = question_service.list_quiz_questions(created_quiz_a.id)
    quiz_b_questions = question_service.list_quiz_questions(created_quiz_b.id)

    assert len(quiz_a_questions) == 2
    assert len(quiz_b_questions) == 1

def test_list_questions_for_missing_quiz(db_session):
    quiz_repository = QuizRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)

    question_service = QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

    with pytest.raises(ValueError, match='Quiz not found'):
        question_service.list_quiz_questions(quiz_id=999999)




