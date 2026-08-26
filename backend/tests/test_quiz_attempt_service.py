

from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.repositories.quiz_attempt_answer_repository import QuizAttemptAnswerRepository
from backend.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from backend.app.services.quiz_attempt_service import QuizAttemptService

from backend.app.models.user import User, UserRole
from backend.app.models.course import Course
from backend.app.models.quiz import Quiz
from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption



from backend.app.core.security import hash_password
from datetime import datetime
from typing import Optional
import pytest
import uuid
import random

def create_test_environment(db_session, include_teacher: Optional[bool] = False):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    course_enrollment_repository = CourseEnrollmentRepository(db_session)
    course_enrollment_service = CourseEnrollmentService(enrollment_repository=course_enrollment_repository, course_repository=course_repository)
    quiz_repository = QuizRepository(db_session)
    quiz_attempt_repository = QuizAttemptRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)
    answer_repository = QuizAttemptAnswerRepository(db_session)
    quiz_attempt_service = QuizAttemptService(attempt_repository=quiz_attempt_repository, quiz_repository=quiz_repository, enrollment_repository=course_enrollment_repository, question_repository=question_repository, answer_repository=answer_repository)

    uid = uuid.uuid4().hex[:8]

    teacher = user_repository.create(User(email=f'test_teacher_email_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Teacher', role=UserRole.TEACHER))
    student = user_repository.create(User(email=f'test_student_email_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Student', role=UserRole.STUDENT))
    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    course = course_service.publish_course(course_id=course.id)
    student_course_enrollment = course_enrollment_service.enroll(student_id=student.id, course_id=course.id)
    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))

    if include_teacher:
        return teacher, student, quiz, quiz_attempt_service
    else:

        return student, quiz, quiz_attempt_service




def create_test_student(db_session):
    user_repository = UserRepository(db_session)

    uid = uuid.uuid4().hex[:8]

    student = user_repository.create(User(email=f'test_student_email_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Student', role=UserRole.STUDENT))

    return student

def create_question_options_and_start_attempt(db_session, student: User, quiz: Quiz, quiz_attempt_service: QuizAttemptService):

    uid = uuid.uuid4().hex[:8]

    if student is None:
        raise ValueError('Student cannot be None')

    if quiz is None:
        raise ValueError('Quiz cannot be None')

    if quiz_attempt_service is None:
        raise ValueError('QuizAttemptService cannot be None')

    question_repository = QuizQuestionRepository(db_session)
    question = QuizQuestion(question_text=f'Test Question {uid}', quiz_id=quiz.id)
    question = question_repository.create_question(quiz_question=question)

    option_one = QuizOption(option_text=f'Test Option One {uid}', question_id=question.id, is_correct=True)
    option_two = QuizOption(option_text=f'Test Option Two {uid}', question_id=question.id, is_correct=False)
    option_three = QuizOption(option_text=f'Test Option Three {uid}', question_id=question.id, is_correct=False)

    option_one = question_repository.create_option(option_one)
    option_two = question_repository.create_option(option_two)
    option_three = question_repository.create_option(option_three)

    student_attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)


    student_id = student.id
    attempt_id = student_attempt.id
    question_id = question.id
    selected_option_id = option_one.id



    return  student_id, attempt_id, question_id, selected_option_id

def create_attempt_and_submit_answer(db_session, student: User, quiz: Quiz, quiz_attempt_service: QuizAttemptService):
    if student is None:
        return None

    if student.role != UserRole.STUDENT:
        return None
    student_id, attempt_id, question_id, selected_option_id = create_question_options_and_start_attempt(db_session, student, quiz, quiz_attempt_service)

    quiz_attempt_service.submit_answer(student_id=student_id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

    return attempt_id


def create_question_and_options(db_session, student: User, quiz: Quiz, quiz_attempt_service: QuizAttemptService):



    if student is None:
        raise ValueError('Student cannot be None')

    if quiz is None:
        raise ValueError('Quiz cannot be None')

    if quiz_attempt_service is None:
        raise ValueError('QuizAttemptService cannot be None')


    question_repository = QuizQuestionRepository(db_session)
    question = QuizQuestion(question_text=f'Test Question {random.randint}', quiz_id=quiz.id)
    question = question_repository.create_question(quiz_question=question)



    option_one = QuizOption(option_text=f'Test Option One {question.id}', question_id=question.id, is_correct=True)
    option_two = QuizOption(option_text=f'Test Option Two {question.id}', question_id=question.id, is_correct=False)
    option_three = QuizOption(option_text=f'Test Option Three {question.id}', question_id=question.id, is_correct=False)

    option_one = question_repository.create_option(option_one)
    option_two = question_repository.create_option(option_two)
    option_three = question_repository.create_option(option_three)



    question_id = question.id
    selected_option_id = option_one.id



    return question_id, selected_option_id





def create_test_environment_without_enrollment(db_session):

    user_repository = UserRepository(db_session)
    course_repository = CourseRepository(db_session)
    course_service = CourseService(course_repository)
    course_enrollment_repository = CourseEnrollmentRepository(db_session)
    course_enrollment_service = CourseEnrollmentService(enrollment_repository=course_enrollment_repository, course_repository=course_repository)
    quiz_repository = QuizRepository(db_session)
    quiz_attempt_repository = QuizAttemptRepository(db_session)
    question_repository = QuizQuestionRepository(db_session)
    answer_repository = QuizAttemptAnswerRepository(db_session)
    quiz_attempt_service = QuizAttemptService(attempt_repository=quiz_attempt_repository, quiz_repository=quiz_repository, enrollment_repository=course_enrollment_repository, question_repository=question_repository, answer_repository=answer_repository)

    uid = uuid.uuid4().hex[:8]

    teacher = user_repository.create(User(email=f'test_teacher_email_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Teacher', role=UserRole.TEACHER))
    student = user_repository.create(User(email=f'test_student_email_{uid}@example.com', hashed_password=hash_password('SuperSecretPassword123!'), full_name='Test Student', role=UserRole.STUDENT))
    course = course_repository.create(Course(title=f'Test Course {uid}', description='Test Course Description', teacher_id=teacher.id))
    course = course_service.publish_course(course_id=course.id)
    quiz = quiz_repository.create(Quiz(title=f'Test Quiz {uid}', description='Test Quiz Description', course_id=course.id))

    return student, quiz, quiz_attempt_service

def test_student_can_start_quiz_attempt(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    assert attempt is not None
    assert attempt.student_id == student.id
    assert attempt.quiz_id == quiz.id

def test_student_cannot_start_attempt_without_enrollment(db_session):
    student, quiz, quiz_attempt_service = create_test_environment_without_enrollment(db_session)

    with pytest.raises(ValueError, match='Enrollment not found'):
        quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

def test_start_attempt_for_missing_quiz(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    with pytest.raises(ValueError, match='Quiz not found'):
        quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=999999)

def test_get_attempt(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    created_attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    assert created_attempt is not None
    assert created_attempt.student_id == student.id
    assert created_attempt.quiz_id == quiz.id

    retrieved_attempt = quiz_attempt_service.get_attempt(attempt_id=created_attempt.id)

    assert retrieved_attempt is not None
    assert retrieved_attempt.id == created_attempt.id

def test_get_missing_attempt(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    with pytest.raises(ValueError, match='Attempt not found'):
        quiz_attempt_service.get_attempt(attempt_id=999999)

def test_list_student_attempts(db_session):
    student_a, quiz_a, quiz_attempt_service = create_test_environment(db_session)
    student_b, quiz_b, quiz_attempt_service = create_test_environment(db_session)

    student_a_attempt_one = quiz_attempt_service.start_attempt(student_id=student_a.id, quiz_id=quiz_a.id)
    student_a_attempt_two = quiz_attempt_service.start_attempt(student_id=student_a.id, quiz_id=quiz_a.id)

    assert student_a_attempt_one.quiz_id == quiz_a.id
    assert student_a_attempt_two.quiz_id == quiz_a.id

    student_b_attempt_one = quiz_attempt_service.start_attempt(student_id=student_b.id, quiz_id=quiz_b.id)

    assert student_b_attempt_one.quiz_id == quiz_b.id

    student_a_attempts = quiz_attempt_service.list_student_attempts(student_id=student_a.id)
    student_b_attempts = quiz_attempt_service.list_student_attempts(student_id=student_b.id)

    assert len(student_a_attempts) == 2
    assert len(student_b_attempts) == 1


def test_student_can_submit_answer(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    student_id, attempt_id, question_id, selected_option_id = create_question_options_and_start_attempt(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)

    submitted_answer = quiz_attempt_service.submit_answer(attempt_id=attempt_id, student_id=student_id, question_id=question_id, selected_option_id=selected_option_id)

    assert submitted_answer is not None
    assert submitted_answer.attempt_id == attempt_id
    assert submitted_answer.question_id == question_id
    assert submitted_answer.selected_option_id == selected_option_id

def test_student_cannot_submit_answer_to_another_students_attempt(db_session):
    student_a, quiz, quiz_attempt_service = create_test_environment(db_session)
    student_a_id, attempt_id, question_id, selected_option_id = create_question_options_and_start_attempt(db_session, student=student_a, quiz=quiz, quiz_attempt_service=quiz_attempt_service)
    student_b = create_test_student(db_session)

    with pytest.raises(ValueError, match='You do not have access to this attempt'):
        quiz_attempt_service.submit_answer(student_id=student_b.id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

    student_a_submits_answer = quiz_attempt_service.submit_answer(student_id=student_a.id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

    assert student_a_submits_answer is not None
    assert student_a_submits_answer.attempt_id == attempt_id
    assert student_a_submits_answer.question_id == question_id
    assert student_a_submits_answer.selected_option_id == selected_option_id

def test_cannot_submit_answer_to_completed_attempt(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    student_id, attempt_id, question_id, selected_option_id = create_question_options_and_start_attempt(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)

    attempt = quiz_attempt_service.get_attempt(attempt_id=attempt_id)

    assert attempt is not None
    assert attempt.completed_at is None

    attempt.completed_at = datetime.now()

    db_session.commit()
    db_session.refresh(attempt)

    assert attempt.completed_at is not None

    attempt_id = attempt.id

    with pytest.raises(ValueError, match='Attempt is already completed'):
        quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)


def test_cannot_submit_question_from_another_quiz(db_session):
    student_a, quiz_a, quiz_attempt_service = create_test_environment(db_session)
    student_b, quiz_b, quiz_attempt_service = create_test_environment(db_session)

    student_a_id, student_a_attempt_id, quiz_a_question_id, question_a_selected_option_id = create_question_options_and_start_attempt(db_session, student=student_a, quiz=quiz_a, quiz_attempt_service=quiz_attempt_service)
    student_b_id, student_b_attempt_id, quiz_b_question_id, question_b_selected_option_id = create_question_options_and_start_attempt(db_session, student=student_b, quiz=quiz_b, quiz_attempt_service=quiz_attempt_service)

    with pytest.raises(ValueError, match='Question does not belong to this quiz'):
        student_a_tries_submitting_question_b_for_quiz_a = quiz_attempt_service.submit_answer(student_id=student_a_id, question_id=quiz_b_question_id, selected_option_id=question_b_selected_option_id, attempt_id=student_a_attempt_id)


def test_cannot_submit_option_from_another_question(db_session):
    student_a, quiz_a, quiz_attempt_service = create_test_environment(db_session)
    student_b, quiz_b, quiz_attempt_service = create_test_environment(db_session)

    student_a_id, student_a_attempt_id, quiz_a_question_id, question_a_selected_option_id = create_question_options_and_start_attempt(db_session, student=student_a, quiz=quiz_a, quiz_attempt_service=quiz_attempt_service)
    student_b_id, student_b_attempt_id, quiz_b_question_id, question_b_selected_option_id = create_question_options_and_start_attempt(db_session, student=student_b, quiz=quiz_b, quiz_attempt_service=quiz_attempt_service)

    with pytest.raises(ValueError, match='Selected option does not belong to this question'):
        quiz_attempt_service.submit_answer(student_id=student_a_id, attempt_id=student_a_attempt_id, question_id=quiz_a_question_id, selected_option_id=question_b_selected_option_id)



def test_cannot_answer_same_question_twice(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    student_id, attempt_id, question_id, selected_option_id = create_question_options_and_start_attempt(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)

    submitted_answer = quiz_attempt_service.submit_answer(student_id=student_id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

    assert submitted_answer.attempt_id == attempt_id
    assert submitted_answer.question_id == question_id
    assert submitted_answer.selected_option_id == selected_option_id

    with pytest.raises(ValueError, match='Question has already been answered'):
        quiz_attempt_service.submit_answer(student_id=student_id, attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

def test_complete_attempt_calculates_score(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    question_one_id, question_one_selected_option_id = create_question_and_options(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)
    question_two_id, question_two_selected_option_id = create_question_and_options(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)
    question_three_id, question_three_selected_option_id = create_question_and_options(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)
    question_four_id, question_four_selected_option_id = create_question_and_options(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    question_one_submit = quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_one_id, selected_option_id=question_one_selected_option_id)

    assert question_one_submit is not None

    question_two_submit = quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_two_id, selected_option_id=question_two_selected_option_id)

    assert question_two_submit is not None

    question_three_submit = quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_three_id, selected_option_id=question_three_selected_option_id + 1)

    assert question_three_submit is not None

    question_four_submit = quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_four_id, selected_option_id=question_four_selected_option_id)

    assert question_four_submit is not None

    completed_attempt = quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

    assert completed_attempt is not None
    assert completed_attempt.id == attempt.id
    assert completed_attempt.score == 75.0
    assert completed_attempt.completed_at is not None

def test_complete_attempt_counts_unanswered_questions_as_incorrect(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    questions_and_options = []


    for i in range(4):
        question_id, selected_option_id = create_question_and_options(db_session, student=student, quiz=quiz, quiz_attempt_service=quiz_attempt_service)

        questions_and_options.append((question_id, selected_option_id))


    question_one_id, question_one_selected_option_id = questions_and_options[0]
    question_two_id, question_two_selected_option_id = questions_and_options[1]
    question_three_id, question_three_selected_option_id = questions_and_options[2]
    question_four_id, question_four_selected_option_id = questions_and_options[3]

    question_repository = QuizQuestionRepository(db_session)


    question_three_options = question_repository.list_options(question_id=question_three_id)
    question_four_options = question_repository.list_options(question_id=question_four_id)

    question_three_incorrect_option = question_three_options[1].id
    question_four_incorrect_option = question_four_options[1].id

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_one_id, selected_option_id=question_one_selected_option_id)
    quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_two_id, selected_option_id=question_two_selected_option_id)
    quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_three_id, selected_option_id=question_three_incorrect_option)
    quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_four_id, selected_option_id=question_four_incorrect_option)

    completed_attempt = quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

    assert completed_attempt.score == 50.0



def test_complete_attempt_with_all_correct_answers(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    questions_and_options = []

    for i in range(4):
        question_id, selected_option_id = create_question_and_options(db_session, student, quiz, quiz_attempt_service)
        questions_and_options.append((question_id, selected_option_id))

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    for question_id, selected_option_id in questions_and_options:
        quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_id, selected_option_id=selected_option_id)


    completed_answer = quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

    assert completed_answer.score == 100.0

def test_complete_attempt_with_all_wrong_answers(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    questions_and_options = []
    question_repository = QuizQuestionRepository(db_session)

    for i in range(4):
        question_id, selected_option_id = create_question_and_options(db_session, student, quiz, quiz_attempt_service)
        question_options = question_repository.list_options(question_id=question_id)
        selected_option_id = question_options[1].id
        questions_and_options.append((question_id, selected_option_id))


    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    for question_id, selected_option_id in questions_and_options:
        quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_id, selected_option_id=selected_option_id)


    completed_attempt = quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

    assert completed_attempt.score == 0.0

def test_cannot_complete_attempt_twice(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    question_id, selected_option_id = create_question_and_options(db_session, student, quiz, quiz_attempt_service)

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    quiz_attempt_service.submit_answer(student_id=student.id, attempt_id=attempt.id, question_id=question_id, selected_option_id=selected_option_id)

    quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

    with pytest.raises(ValueError, match='Attempt is already completed'):
        quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt.id)

def test_student_cannot_complete_another_students_attempt(db_session):
    student_a, quiz, quiz_attempt_service = create_test_environment(db_session)
    question_id, selected_option_id = create_question_and_options(db_session, student_a, quiz, quiz_attempt_service)
    student_b = create_test_student(db_session)

    attempt = quiz_attempt_service.start_attempt(student_id=student_a.id, quiz_id=quiz.id)

    quiz_attempt_service.submit_answer(student_a.id, attempt.id, question_id=question_id, selected_option_id=selected_option_id)

    with pytest.raises(ValueError, match='You do not have access to this attempt'):
        quiz_attempt_service.complete_attempt(student_b.id, attempt.id)

def test_cannot_complete_empty_quiz(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    attempt = quiz_attempt_service.start_attempt(student_id=student.id, quiz_id=quiz.id)

    with pytest.raises(ValueError, match='Quiz does not contain any questions'):
        quiz_attempt_service.complete_attempt(student.id, attempt.id)


def test_list_completed_student_attempts(db_session):

    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    attempt_one_id = create_attempt_and_submit_answer(db_session, student, quiz, quiz_attempt_service)
    attempt_two_id = create_attempt_and_submit_answer(db_session, student, quiz, quiz_attempt_service)
    attempt_three_id = create_attempt_and_submit_answer(db_session, student, quiz, quiz_attempt_service)

    quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt_one_id)
    quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt_two_id)

    student_completed_attempts = quiz_attempt_service.list_completed_student_attempts(student.id)

    assert len(student_completed_attempts) == 2

    quiz_attempt_service.complete_attempt(student_id=student.id, attempt_id=attempt_three_id)

    student_complete_attempts = quiz_attempt_service.list_completed_student_attempts(student.id)

    assert len(student_complete_attempts) == 3

def test_list_completed_student_attempts_returns_empty_list(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)

    student_completed_attempts = quiz_attempt_service.list_completed_student_attempts(student.id)

    assert len(student_completed_attempts) == 0

def test_student_history_does_not_include_another_students_attempts(db_session):

    student_a, quiz_a, quiz_attempt_service = create_test_environment(db_session)
    student_b, quiz_b, quiz_attempt_service = create_test_environment(db_session)

    student_a_attempt_id = create_attempt_and_submit_answer(db_session, student_a, quiz_a, quiz_attempt_service)
    student_b_attempt_id = create_attempt_and_submit_answer(db_session, student_b, quiz_b, quiz_attempt_service)

    quiz_attempt_service.complete_attempt(student_id=student_a.id, attempt_id=student_a_attempt_id)
    quiz_attempt_service.complete_attempt(student_id=student_b.id, attempt_id=student_b_attempt_id)

    student_a_history = quiz_attempt_service.list_completed_student_attempts(student_a.id)
    student_b_history = quiz_attempt_service.list_completed_student_attempts(student_b.id)

    assert len(student_a_history) == 1
    assert student_a_history[0].student_id == student_a.id
    assert len(student_b_history) == 1
    assert student_b_history[0].student_id == student_b.id

def test_list_quiz_attempts(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    create_attempt_and_submit_answer(db_session, student, quiz, quiz_attempt_service)
    create_attempt_and_submit_answer(db_session, student, quiz, quiz_attempt_service)

    quiz_attempts = quiz_attempt_service.list_quiz_attempts(quiz.id)

    assert len(quiz_attempts) == 2
    assert quiz_attempts[0].quiz_id == quiz.id
    assert quiz_attempts[1].student_id == student.id


def test_list_quiz_attempts_for_missing_quiz(db_session):
    student, quiz, quiz_attempt_service = create_test_environment(db_session)
    with pytest.raises(ValueError, match='Quiz not found'):
        quiz_attempt_service.list_quiz_attempts(999999)

    quiz_attempts = quiz_attempt_service.list_quiz_attempts(quiz.id)

    assert len(quiz_attempts) == 0








































