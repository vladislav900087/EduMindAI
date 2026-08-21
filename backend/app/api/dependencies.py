from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.user_service import UserService
from backend.app.repositories.course_repository import CourseRepository
from backend.app.services.course_service import CourseService

from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.services.lesson_service import LessonService

from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.services.course_enrollment_service import CourseEnrollmentService

from backend.app.repositories.lesson_progress_repository import LessonProgressRepository
from backend.app.services.lesson_progress_service import LessonProgressService

from backend.app.repositories.quiz_repository import QuizRepository
from backend.app.services.quiz_service import QuizService

from backend.app.repositories.quiz_question_repository import QuizQuestionRepository
from backend.app.services.quiz_question_service import QuizQuestionService

from backend.app.models.user import User
from backend.app.api.authorization import require_course_owner, get_current_user

from backend.app.models.quiz import Quiz



# repository and service dependencies
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

def get_course_enrollment_repository(db: Session = Depends(get_db)) -> CourseEnrollmentRepository:
    return CourseEnrollmentRepository(db=db)

def get_course_enrollment_service(enrollment_repository: CourseEnrollmentRepository = Depends(get_course_enrollment_repository), course_repository: CourseRepository = Depends(get_course_repository)) -> CourseEnrollmentService:
    return CourseEnrollmentService(enrollment_repository=enrollment_repository, course_repository=course_repository)

def get_lesson_progress_repository(db: Session = Depends(get_db)) -> LessonProgressRepository:
    return LessonProgressRepository(db=db)

def get_lesson_progress_service(progress_repository: LessonProgressRepository = Depends(get_lesson_progress_repository), enrollment_repository: CourseEnrollmentRepository = Depends(get_course_enrollment_repository), lesson_repository: LessonRepository = Depends(get_lesson_repository), course_repository: CourseRepository = Depends(get_course_repository)) -> LessonProgressService:

    return LessonProgressService(progress_repository=progress_repository, enrollment_repository=enrollment_repository, lesson_repository=lesson_repository, course_repository=course_repository)

# quiz repository and service
def get_quiz_repository(db: Session = Depends(get_db)) -> QuizRepository:
    return QuizRepository(db=db)

def get_quiz_service(quiz_repository: QuizRepository = Depends(get_quiz_repository)) -> QuizService:
    return QuizService(quiz_repository)

# quiz questions repository and service

def get_quiz_questions_repository(db: Session = Depends(get_db)) -> QuizQuestionRepository:
    return QuizQuestionRepository(db=db)

def get_quiz_questions_service(question_repository: QuizQuestionRepository = Depends(get_quiz_questions_repository), quiz_repository: QuizRepository = Depends(get_quiz_repository)) -> QuizQuestionService:

    return QuizQuestionService(quiz_repository=quiz_repository, question_repository=question_repository)

# management dependencies

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

def get_quiz_for_management(quiz_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    quiz_repository = QuizRepository(db=db)
    course_repository = CourseRepository(db=db)

    quiz = quiz_repository.get_by_id(quiz_id)

    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quiz not found')

    course = course_repository.get_by_id(quiz.course_id)

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

    require_course_owner(course, current_user)

    return quiz




