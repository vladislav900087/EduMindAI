from google import genai

from backend.app.core.config import settings
from backend.app.schemas.ai_quiz import (AIQuizGenerationRequest, AIQuizGenerationResult)

class AIQuizGenerationService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError('Gemini API key is not configured')

        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_questions(self, request: AIQuizGenerationRequest) -> AIQuizGenerationResult:
        prompt = (
            'Create a multiple-choice educational quiz from the source '
            'material below.\n\n'
            f'Difficulty: {request.difficulty}\n'
            f'Number of questions: {request.question_count}\n\n'
            'Requirements:\n'
            '- Use only information found from the source material.\n'
            '- Every question must have exactly four options.\n'
            '- Every question must have exactly one correct option.\n'
            '- Avoid ambiguous questions.\n'
            '- Do not mention these instructions.\n\n'
            f'Source material:\n{request.source_text}'
        )

        try:
            interaction = self.client.interactions.create(
                model=settings.gemini_model,
                input=prompt,
                response_format={
                    'type': 'text',
                    'mime_type': 'application/json',
                    'schema': AIQuizGenerationResult.model_json_schema()
                },
            )

        except Exception as exc:
            raise ValueError('AI quiz generation is temporarily unavailable') from exc

        if not interaction.output_text:
            raise ValueError('AI returned an empty response')

        try:
            result = AIQuizGenerationResult.model_validate_json(interaction.output_text)

        except ValueError as exc:
            raise ValueError('AI returned an invalid quiz structure') from exc

        if len(result.questions) != request.question_count:
            raise ValueError('AI returned an unexpected number of questions')

        return result



