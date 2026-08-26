from fastapi import APIRouter
from backend.app.api.auth import router as auth_router
from backend.app.api.users import router as users_router
from backend.app.api.courses import router as courses_router
from backend.app.api.lessons import router as lessons_router
from backend.app.api.lessons import course_router as lesson_course_router
from backend.app.api.enrollments import router as enrollments_router
from backend.app.api.quizzes import (router as quiz_router, course_router as quiz_course_router)
from backend.app.api.quiz_questions import (router as quiz_question_router, question_router)
from backend.app.api.quiz_attempts import router as quiz_attempt_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(courses_router)
router.include_router(lessons_router)
router.include_router(lesson_course_router)
router.include_router(enrollments_router)
router.include_router(quiz_router)
router.include_router(quiz_course_router)
router.include_router(quiz_question_router)
router.include_router(question_router)
router.include_router(quiz_attempt_router)

@router.get('/health')
def health_check():
    return {'status': 'ok'}