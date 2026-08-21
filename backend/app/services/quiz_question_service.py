from backend.app.models.quiz_question import QuizQuestion
from backend.app.models.quiz_option import QuizOption
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.schemas.quiz_question import QuizQuestionCreate


class QuizQuestionService:
    def __init__(self, question_repository: QuizQuestionRepository, quiz_repository: QuizRepository):
        self.question_repository = question_repository
        self.quiz_repository = quiz_repository

    def create_question(self, quiz_id: int, question_data: QuizQuestionCreate) -> QuizQuestion:
        quiz = self.quiz_repository.get_by_id(quiz_id)

        if quiz is None:
            raise ValueError('Quiz not found')

        if len(question_data.options) < 2:
            raise ValueError('A question must have at least 2 options')

        correct_options = [option for option in question_data.options if option.is_correct]

        if len(correct_options) != 1:
            raise ValueError('A question must have exactly 1 correct option')


        question = self.question_repository.create_question(QuizQuestion(question_text=question_data.question_text, quiz_id=quiz_id))

        for option_data in question_data.options:
            option = QuizOption(option_text=option_data.option_text, question_id=question.id, is_correct=option_data.is_correct)

            self.question_repository.create_option(option)

        return question

    def get_question(self, question_id: int) -> QuizQuestion:
        question = self.question_repository.get_by_id(question_id)

        if question is None:
            raise ValueError('Question not found')

        return question

    def list_quiz_questions(self, quiz_id: int) -> list[QuizQuestion]:

        quiz = self.quiz_repository.get_by_id(quiz_id)

        if quiz is None:
            raise ValueError('Quiz not found')

        questions = self.question_repository.list_by_quiz(quiz_id)

        return questions




