from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_quiz_service, get_course_for_management
from backend.app.services.quiz_service import QuizService
from backend.app.models.user import User, UserRole
from backend.app.schemas.quiz import QuizCreate, QuizRead


router = APIRouter(prefix='/quizzes', tags=['Quizzes'])
course_router = APIRouter(prefix='/courses', tags=['Quizzes'])

@course_router.post('/{course_id}/quizzes', response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(course_id: int, quiz_data: QuizCreate, course=Depends(get_course_for_management), service: QuizService = Depends(get_quiz_service)):
    return service.create_quiz(course_id=course_id, quiz_data=quiz_data)

@course_router.get('/{course_id}/quizzes', response_model=list[QuizRead], status_code=status.HTTP_200_OK)
def list_course_quizzes(course_id: int, course=Depends(get_course_for_management), service: QuizService = Depends(get_quiz_service)):

    return service.list_course_quizzes(course_id=course_id)

@router.get('/{quiz_id}', response_model=QuizRead, status_code=status.HTTP_200_OK)
def get_quiz(quiz_id: int, service: QuizService = Depends(get_quiz_service)):
    try:
        return service.get_quiz(quiz_id=quiz_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc



