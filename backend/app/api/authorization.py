from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from backend.app.api.security import get_current_user
from backend.app.models.user import User, UserRole


def require_roles(*allowed_roles: UserRole) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have permission to perform this action.')

        return current_user

    return role_checker

def require_course_owner(course, user):
    if user.role == UserRole.ADMIN:
        return user

    if user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only teachers can manage course content')

    if course.teacher_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not own this course')

    return user


