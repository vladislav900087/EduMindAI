from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_lesson_service, get_course_for_management
from backend.app.schemas.lesson import LessonCreate, LessonRead
from backend.app.services.lesson_service import LessonService



router = APIRouter(prefix='/lessons', tags=['Lessons'])

course_router = APIRouter(prefix='/courses', tags=['Lessons'])

@course_router.post('/{course_id}/lessons', response_model=LessonRead, status_code=status.HTTP_201_CREATED)
def create_lesson(course_id: int, lesson_data: LessonCreate, course = Depends(get_course_for_management), service: LessonService = Depends(get_lesson_service)):
    try:
        return service.create_lesson(course_id=course_id, lesson_data=lesson_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

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


@router.delete('/{lesson_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, service: LessonService = Depends(get_lesson_service)):
    try:
        return service.delete_lesson(lesson_id=lesson_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


