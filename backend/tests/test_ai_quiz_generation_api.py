from backend.app.api.dependencies import get_ai_quiz_generation_service
from backend.app.main import app
from backend.app.models.user import UserRole
from backend.app.schemas.ai_quiz import AIQuizGenerationResult
from backend.tests.test_quiz_questions_api import (
    create_test_course_and_quiz,
    create_test_user_and_get_token
)


class FakeAIQuizGenerationService:
    def generate_questions(self, request) -> AIQuizGenerationResult:
        return AIQuizGenerationResult(
            questions=[
                {
                    'question_text': 'What is the correct answer?',
                    'options': [
                        {
                            'option_text': 'Option A',
                            'is_correct': True,
                        },
                        {
                            'option_text': 'Option B',
                            'is_correct': False,

                        },
                        {
                            'option_text': 'Option C',
                            'is_correct': False,
                        },
                        {'option_text': 'Option D',
                         'is_correct': False,

                         }
                    ]
                }
            ]
        )


def override_ai_service():
    return FakeAIQuizGenerationService()

def test_teacher_can_generate_question_preview(db_session, client):
    teacher, token = create_test_user_and_get_token(
        db_session,
        client,
        UserRole.TEACHER
    )

    _, quiz = create_test_course_and_quiz(db_session, teacher)

    app.dependency_overrides[get_ai_quiz_generation_service] = override_ai_service

    try:
        response = client.post(
            f'/quizzes/{quiz.id}/generate-questions',
            headers={"Authorization": f'Bearer {token}'},
            json={
                'source_text': (
                    'This is sufficiently long educational material.'
                ),
                'question_count': 1,
                'difficulty': 'medium',

            },
        )
    finally:
        app.dependency_overrides.pop(get_ai_quiz_generation_service, None)


    assert response.status_code == 200
    assert len(response.json()['questions']) == 1
    assert len(response.json()['questions'][0]['options']) == 4


def test_student_cannot_generate_questions(db_session, client):
    teacher, _ = create_test_user_and_get_token(
        db_session,
        client,
        UserRole.TEACHER
    )

    student, student_token = create_test_user_and_get_token(
        db_session,
        client,
        UserRole.STUDENT
    )

    _, quiz = create_test_course_and_quiz(db_session, teacher)

    app.dependency_overrides[get_ai_quiz_generation_service] = override_ai_service

    try:
        response = client.post(
            f'/quizzes/{quiz.id}/generate-questions',
            headers={'Authorization': f'Bearer {student_token}'},
            json={
                'source_text': (
                    'This is sufficiently long educational material.'
                ),
                'question_count': 1,
                'difficulty': 'medium'
            }
        )

    finally:
        app.dependency_overrides.pop(get_ai_quiz_generation_service, None)

    assert student.id is not None
    assert response.status_code == 403





