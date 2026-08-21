from backend.app.models.quiz import Quiz
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.schemas.quiz import QuizCreate


class QuizService:
    def __init__(self, repository: QuizRepository):
        self.repository = repository

    def create_quiz(self, course_id: int, quiz_data: QuizCreate) -> Quiz:
        quiz = Quiz(title=quiz_data.title, course_id=course_id, description=quiz_data.description)

        return self.repository.create(quiz)

    def get_quiz(self, quiz_id: int) -> Quiz:
        quiz = self.repository.get_by_id(quiz_id=quiz_id)
        if quiz is None:
            raise ValueError('Quiz not found')

        return quiz

    def list_course_quizzes(self, course_id: int) -> list[Quiz]:
        return self.repository.list_by_course(course_id=course_id)


