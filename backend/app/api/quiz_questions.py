from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import (get_quiz_for_management, get_quiz_questions_service, get_ai_quiz_generation_service)
from backend.app.schemas.quiz_question import (QuizQuestionCreate, QuizQuestionRead)
from backend.app.schemas.ai_quiz import (
    AIQuizGenerationRequest,
    AIQuizGenerationResult,

)

from backend.app.services.ai_quiz_generation_service import AIQuizGenerationService
from backend.app.services.quiz_question_service import QuizQuestionService



router = APIRouter(prefix='/quizzes', tags=['Quiz Questions'])
question_router = APIRouter(prefix='/questions', tags=['Quiz Questions'])

@router.post('/{quiz_id}/questions', status_code=status.HTTP_201_CREATED, response_model=QuizQuestionRead)
def create_question(quiz_id: int, question_data: QuizQuestionCreate, quiz=Depends(get_quiz_for_management), service: QuizQuestionService = Depends(get_quiz_questions_service)):
    try:
        return service.create_question(quiz_id=quiz_id, question_data=question_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

@router.post('/{quiz_id}/generate-questions', response_model=AIQuizGenerationResult, status_code=status.HTTP_200_OK)
def generate_quiz_questions(
        quiz_id: int,
        generation_request: AIQuizGenerationRequest,
        quiz=Depends(get_quiz_for_management),
        service: AIQuizGenerationService = Depends(get_ai_quiz_generation_service)
):
    try:
        return service.generate_questions(request=generation_request)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    

@router.get('/{quiz_id}/questions', status_code=status.HTTP_200_OK, response_model=list[QuizQuestionRead])
def list_quiz_questions(quiz_id: int, service: QuizQuestionService = Depends(get_quiz_questions_service)):
    try:
        return service.list_quiz_questions(quiz_id=quiz_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@question_router.get('/{question_id}', status_code=status.HTTP_200_OK, response_model=QuizQuestionRead)
def get_question(question_id: int, service: QuizQuestionService = Depends(get_quiz_questions_service)):
    try:
        return service.get_question(question_id=question_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc



