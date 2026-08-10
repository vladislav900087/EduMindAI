from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.authorization import require_roles
from backend.app.api.security import get_current_user
from backend.app.models.user import User, UserRole
from backend.app.schemas.course import CourseCreate, CourseRead
from backend.app.services.course_service import CourseService
from backend.app.api.dependencies import get_course_service


router = APIRouter(prefix='/courses', tags=['Courses'])

@router.post('', response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, current_user: User = Depends(require_roles(UserRole.TEACHER, UserRole.ADMIN)), service: CourseService = Depends(get_course_service)):
    return service.create_course(course_data, current_user)


@router.get('', response_model=list[CourseRead], status_code=status.HTTP_200_OK)
def list_courses(service: CourseService = Depends(get_course_service)):
    return service.list_courses()



@router.get('/my', response_model=list[CourseRead], status_code=status.HTTP_200_OK)
def list_my_courses(current_user: User = Depends(require_roles(UserRole.TEACHER, UserRole.ADMIN)), service: CourseService = Depends(get_course_service)):
    return service.list_teacher_courses(teacher_id=current_user.id)


@router.get('/{course_id}', response_model=CourseRead, status_code=status.HTTP_200_OK)
def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    try:
        return service.get_course(course_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc




