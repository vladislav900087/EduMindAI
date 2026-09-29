import pytest

from backend.app.schemas.ai_quiz import (AIQuizGenerationRequest, AIQuizGenerationResult)

from backend.app.services.ai_quiz_generation_service import AIQuizGenerationService


class FakeInteractions:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs

        if self.error:
            raise self.error

        return FakeInteraction(self.output_text)

class FakeInteraction:
    def __init__(self, output_text=None):
        self.output_text = output_text

class FakeClient:
    def __init__(self, output_text=None, error=None):
        self.interactions = FakeInteractions(output_text, error)


def make_request(question_count=1):
    return AIQuizGenerationRequest(
        source_text=(
            'Python is a programming language used for many different software tasks'
        ),
        question_count=question_count,
        difficulty='medium'

    )

def make_valid_result():

    return AIQuizGenerationResult(
        questions=[
            {
                'question_text': 'What is Python?',
                'options': [
                    {
                        'option_text': 'A programming language',
                        'is_correct': True
                    },
                    {
                        'option_text': 'A database',
                        'is_correct': False
                    },
                    {
                        'option_text': 'An operating system',
                        'is_correct': False
                    },
                    {
                        'option_text': 'A web-browser',
                        'is_correct': False
                    },
                ],
            }
        ]
    )

def test_generate_questions_returns_validated_result():

    fake_client = FakeClient(
        output_text=make_valid_result().model_dump_json()
    )

    service = AIQuizGenerationService(client=fake_client)
    result = service.generate_questions(make_request())

    assert len(result.questions) == 1
    assert len(result.questions[0].options) == 4
    assert result.questions[0].options[0].is_correct is True

    sent_request = fake_client.interactions.last_request
    assert sent_request['input']
    assert sent_request['response_format']['mime_type'] == (
        'application/json'
    )


def test_generate_questions_handles_provider_failure():
    fake_client = FakeClient(error=RuntimeError('Provider unavailable'))
    service = AIQuizGenerationService(client=fake_client)

    with pytest.raises(
        ValueError,
        match='AI quiz generation is temporarily unavailable'
    ):
        service.generate_questions(make_request())


def test_generate_questions_returns_empty_response():
    fake_client = FakeClient(output_text=None)
    service = AIQuizGenerationService(client=fake_client)

    with pytest.raises(
        ValueError,
        match='AI returned an empty response'
    ):
        service.generate_questions(make_request())

def test_generate_questions_rejects_invalid_json():
    fake_client = FakeClient(output_text=make_valid_result())
    service = AIQuizGenerationService(client=fake_client)

    with pytest.raises(
        ValueError,
        match='AI returned an invalid quiz structure'
    ):
        service.generate_questions(make_request())


def test_generate_questions_rejects_wrong_question_count():
    fake_client = FakeClient(output_text=make_valid_result().model_dump_json())

    service = AIQuizGenerationService(client=fake_client)

    with pytest.raises(
        ValueError,
        match='AI returned an unexpected number of questions'
    ):
        service.generate_questions(make_request(question_count=2))






