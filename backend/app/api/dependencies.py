from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService

from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.services.lesson_service import LessonService

from backend.app.models.user import User
from backend.app.api.authorization import require_course_owner, get_current_user


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)

def get_course_repository(db: Session = Depends(get_db)) -> CourseRepository:
    return CourseRepository(db=db)

def get_course_service(repository: CourseRepository = Depends(get_course_repository)) -> CourseService:
    return CourseService(repository=repository)

def get_lesson_repository(db: Session = Depends(get_db)) -> LessonRepository:
    return LessonRepository(db=db)

def get_lesson_service(lesson_repository: LessonRepository = Depends(get_lesson_repository), course_repository: CourseRepository = Depends(get_course_repository)) -> LessonService:
    return LessonService(lesson_repository=lesson_repository, course_repository=course_repository)

def get_course_for_management(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course_repository = CourseRepository(db=db)

    course = course_repository.get_by_id(course_id)

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    require_course_owner(course, current_user)

    return course

def get_lesson_for_management(lesson_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson_repository = LessonRepository(db=db)
    course_repository = CourseRepository(db=db)

    lesson = lesson_repository.get_by_id(lesson_id)

    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lesson not found')

    course = course_repository.get_by_id(lesson.course_id)

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    require_course_owner(course, current_user)

    return lesson



