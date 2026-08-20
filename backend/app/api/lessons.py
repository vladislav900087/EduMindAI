from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_lesson_service, get_course_for_management, get_lesson_for_management, get_lesson_progress_service
from backend.app.api.security import get_current_user
from backend.app.models.user import User, UserRole
from backend.app.schemas.lesson_progress import LessonProgressRead

from backend.app.schemas.lesson import LessonCreate, LessonRead
from backend.app.services.lesson_service import LessonService
from backend.app.services.lesson_progress_service import LessonProgressService





router = APIRouter(prefix='/lessons', tags=['Lessons'])

course_router = APIRouter(prefix='/courses', tags=['Lessons'])

@course_router.post('/{course_id}/lessons', response_model=LessonRead, status_code=status.HTTP_201_CREATED)
def create_lesson(course_id: int, lesson_data: LessonCreate, course = Depends(get_course_for_management), service: LessonService = Depends(get_lesson_service)):
    try:
        return service.create_lesson(course_id=course_id, lesson_data=lesson_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

@router.post('/{lesson_id}/complete', response_model=LessonProgressRead, status_code=status.HTTP_201_CREATED)
def complete_lesson(lesson_id: int, current_user: User = Depends(get_current_user), service: LessonProgressService = Depends(get_lesson_progress_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only student can complete lessons')

    try:
        return service.mark_lesson_complete(student_id=current_user.id, lesson_id=lesson_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc



@course_router.get('/{course_id}/lessons', response_model=list[LessonRead], status_code=status.HTTP_200_OK)
def list_course_lessons(course_id: int, service: LessonService = Depends(get_lesson_service)):
    try:
        return service.list_course_lessons(course_id=course_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

@router.get('/{lesson_id}', response_model=LessonRead, status_code=status.HTTP_200_OK)
def get_lesson(lesson_id: int, service: LessonService = Depends(get_lesson_service)):
    try:
        return service.get_lesson(lesson_id=lesson_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

@router.get('/progress/me', response_model=list[LessonProgressRead], status_code=status.HTTP_200_OK)
def get_my_progress(current_user: User = Depends(get_current_user), service: LessonProgressService = Depends(get_lesson_progress_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can view lesson progress')

    return service.list_student_progress(student_id=current_user.id)


@router.delete('/{lesson_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, service: LessonService = Depends(get_lesson_service), lesson = Depends(get_lesson_for_management)):
    try:
        return service.delete_lesson(lesson_id=lesson_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


