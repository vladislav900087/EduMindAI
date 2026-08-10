from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repository)

def get_course_repository(db: Session = Depends(get_db)) -> CourseRepository:
    return CourseRepository(db=db)

def get_course_service(repository: CourseRepository = Depends(get_course_repository)) -> CourseService:
    return CourseService(repository=repository)

