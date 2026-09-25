import pytest
from pydantic import ValidationError
from backend.app.schemas.ai_quiz import AIQuizQuestion


def test_ai_question_accepts_one_correct_option():

    question = AIQuizQuestion(
        question_text='What is 2 + 2?',
        options=[
            {'option_text': '3', 'is_correct': False},
            {'option_text': '4', 'is_correct': True},
            {'option_text': '5', 'is_correct': False},
            {'option_text': '6', 'is_correct': False}
        ]
    )

    assert len(question.options) == 4


def test_ai_question_rejects_two_correct_options():

    with pytest.raises(ValidationError):
        AIQuizQuestion(
            question_text='Choose the answer:',
            options=[
                {'option_text': 'A', 'is_correct': True},
                {'option_text': 'B', 'is_correct': True},
                {'option_text': 'C', 'is_correct': False},
                {'option_text': 'D', 'is_correct': False}
            ]
        )


def test_ai_question_rejects_no_correct_options():
    with pytest.raises(ValidationError):
        AIQuizQuestion(
            question_text='Choose the answer:',
            options=[
                {'option_text': 'A', 'is_correct': False},
                {"option_text": 'B', 'is_correct': False},
                {'option_text': 'C', 'is_correct': False},
                {'option_text': 'D', 'is_correct': False}
            ]
        )

