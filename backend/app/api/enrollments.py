from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_course_enrollment_service
from backend.app.api.security import get_current_user
from backend.app.models.user import User, UserRole
from backend.app.schemas.course_enrollment import EnrollmentRead
from backend.app.services.course_enrollment_service import CourseEnrollmentService

router = APIRouter(
    prefix='/enrollments',
    tags=['Enrollments']
)

@router.post('/courses{course_id}/enroll', response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll_in_course(course_id: int, current_user: User = Depends(get_current_user), service: CourseEnrollmentService = Depends(get_course_enrollment_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can enroll in courses')

    try:
        return service.enroll(student_id=current_user.id, course_id=course_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

@router.get('/me', response_model=list[EnrollmentRead], status_code=status.HTTP_200_OK)
def get_my_enrollments(current_user: User = Depends(get_current_user), service: CourseEnrollmentService = Depends(get_course_enrollment_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can enroll in courses')

    return service.list_student_enrollments(student_id=current_user.id)


@router.delete('/courses/{course_id}/unenroll', status_code=status.HTTP_204_NO_CONTENT)
def unenroll_from_course(course_id: int, current_user: User = Depends(get_current_user), service: CourseEnrollmentService = Depends(get_course_enrollment_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can enroll in courses')

    try:
        service.unenroll(student_id=current_user.id, course_id=course_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


