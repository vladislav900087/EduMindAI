from backend.app.models.quiz_attempt import QuizAttempt
from backend.app.models.quiz_attempt_answer import QuizAttemptAnswer

from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.quiz_attempt_repository import QuizAttemptRepository
from backend.app.repositories.quiz_attempt_answer_repository import QuizAttemptAnswerRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository

from datetime import datetime, timezone

class QuizAttemptService:
    def __init__(self, attempt_repository: QuizAttemptRepository, quiz_repository: QuizRepository, enrollment_repository: CourseEnrollmentRepository, answer_repository: QuizAttemptAnswerRepository, question_repository: QuizQuestionRepository):

        self.attempt_repository = attempt_repository
        self.quiz_repository = quiz_repository
        self.enrollment_repository = enrollment_repository
        self.question_repository = question_repository
        self.answer_repository = answer_repository


    def start_attempt(self, student_id: int, quiz_id: int) -> QuizAttempt:
        quiz = self.quiz_repository.get_by_id(quiz_id)

        if quiz is None:
            raise ValueError('Quiz not found')

        enrollment = self.enrollment_repository.get_by_student_and_course(student_id=student_id, course_id=quiz.course_id)

        if enrollment is None:
            raise ValueError('Enrollment not found')

        attempt = QuizAttempt(student_id=student_id, quiz_id=quiz_id)

        return self.attempt_repository.create(attempt)

    def submit_answer(self, student_id: int, attempt_id: int, question_id: int, selected_option_id: int) -> QuizAttemptAnswer:
        attempt = self.attempt_repository.get_by_id(attempt_id)

        if attempt is None:
            raise ValueError('Attempt not found')

        if attempt.student_id != student_id:
            raise ValueError('You do not have access to this attempt')

        if attempt.completed_at is not None:
            raise ValueError('Attempt is already completed')

        quiz = self.quiz_repository.get_by_id(attempt.quiz_id)

        if quiz is None:
            raise ValueError('Quiz not found')

        question = self.question_repository.get_by_id(question_id)

        if question is None:
            raise ValueError('Question not found')

        if question.quiz_id != quiz.id:
            raise ValueError('Question does not belong to this quiz')

        options = self.question_repository.list_options(question_id=question_id)

        selected_option = next((option for option in options if option.id == selected_option_id), None)

        if selected_option is None:
            raise ValueError('Selected option does not belong to this question')

        existing_answer = self.answer_repository.get_by_attempt_and_question(attempt_id=attempt_id, question_id=question_id)

        if existing_answer is not None:
            raise ValueError('Question has already been answered')

        answer = QuizAttemptAnswer(attempt_id=attempt_id, question_id=question_id, selected_option_id=selected_option_id)

        return self.answer_repository.create(answer)

    def complete_attempt(self, student_id: int, attempt_id: int) -> QuizAttempt:

        attempt = self.attempt_repository.get_by_id(attempt_id)

        if attempt is None:
            raise ValueError('Attempt not found')

        if attempt.student_id != student_id:
            raise ValueError('You do not have access to this attempt')

        if attempt.completed_at is not None:
            raise ValueError('Attempt is already completed')

        questions = self.question_repository.list_by_quiz(quiz_id=attempt.quiz_id)

        if not questions:
            raise ValueError('Quiz does not contain any questions')

        answers = self.answer_repository.list_by_attempt(attempt_id=attempt_id)

        answers_by_question = {
            answer.question_id: answer for answer in answers
        }

        correct_count = 0

        for question in questions:
            answer = answers_by_question.get(question.id)

            if answer is None:
                continue

            options = self.question_repository.list_options(question_id=question.id)

            selected_option = next((option for option in options if option.id == answer.selected_option_id), None)

            if selected_option is not None and selected_option.is_correct:
                correct_count += 1

        score = (correct_count / len(questions)) * 100

        attempt.score = score
        attempt.completed_at = datetime.now(timezone.utc)

        return self.attempt_repository.update(attempt)

    def list_completed_student_attempts(self, student_id: int) -> list[QuizAttempt]:

        attempts = self.attempt_repository.list_by_student(student_id=student_id)

        completed_attempts = [attempt for attempt in attempts if attempt.completed_at is not None]

        return completed_attempts









    def get_attempt(self, attempt_id: int) -> QuizAttempt:
        attempt = self.attempt_repository.get_by_id(attempt_id=attempt_id)

        if attempt is None:
            raise ValueError('Attempt not found')

        return attempt

    def list_student_attempts(self, student_id: int) -> list[QuizAttempt]:

        return self.attempt_repository.list_by_student(student_id=student_id)

    def list_quiz_attempts(self, quiz_id: int) -> list[QuizAttempt]:
        quiz = self.quiz_repository.get_by_id(quiz_id=quiz_id)

        if quiz is None:
            raise ValueError('Quiz not found')

        return self.attempt_repository.list_by_quiz(quiz_id=quiz_id)




