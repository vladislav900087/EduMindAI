from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.authorization import require_roles
from backend.app.api.security import get_current_user
from backend.app.models.user import User, UserRole
from backend.app.schemas.course import CourseCreate, CourseRead
from backend.app.schemas.lesson_progress import CourseProgressRead
from backend.app.services.course_service import CourseService
from backend.app.services.lesson_progress_service import LessonProgressService
from backend.app.api.dependencies import get_course_service, get_course_for_management, get_lesson_progress_service


router = APIRouter(prefix='/courses', tags=['Courses'])

@router.post('', response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, current_user: User = Depends(require_roles(UserRole.TEACHER, UserRole.ADMIN)), service: CourseService = Depends(get_course_service)):
    return service.create_course(course_data, current_user)


@router.post('/{course_id}/publish', response_model=CourseRead, status_code=status.HTTP_200_OK)
def publish_course(course_id: int, course=Depends(get_course_for_management), service: CourseService = Depends(get_course_service)):
    try:
        return service.publish_course(course_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get('', response_model=list[CourseRead], status_code=status.HTTP_200_OK)
def list_courses(service: CourseService = Depends(get_course_service)):
    return service.list_courses()



@router.get('/my', response_model=list[CourseRead], status_code=status.HTTP_200_OK)
def list_my_courses(current_user: User = Depends(require_roles(UserRole.TEACHER, UserRole.ADMIN)), service: CourseService = Depends(get_course_service)):
    return service.list_teacher_courses(teacher_id=current_user.id)


@router.get('/{course_id}/progress', response_model=CourseProgressRead, status_code=status.HTTP_200_OK)
def get_course_progress(course_id: int, current_user: User = Depends(get_current_user),
                        service: LessonProgressService = Depends(get_lesson_progress_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can view course progress')

    try:
        return service.get_course_progress(course_id=course_id, student_id=current_user.id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get('/{course_id}', response_model=CourseRead, status_code=status.HTTP_200_OK)
def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    try:
        return service.get_course(course_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc







