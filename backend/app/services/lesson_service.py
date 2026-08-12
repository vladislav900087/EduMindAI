from backend.app.models.lesson import Lesson
from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.lesson import LessonCreate


class LessonService:
    def __init__(self, lesson_repository: LessonRepository, course_repository: CourseRepository):
        self.lesson_repository = lesson_repository
        self.course_repository = course_repository

    def create_lesson(self, lesson_data: LessonCreate, course_id: int) -> Lesson:
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError('Course not found')
        lesson = Lesson(title=lesson_data.title, content=lesson_data.content, course_id=course_id)

        return self.lesson_repository.create(lesson)

    def get_lesson(self, lesson_id: int) -> Lesson:
        lesson = self.lesson_repository.get_by_id(lesson_id)
        if lesson is None:
            raise ValueError('Lesson not found')

        return lesson

    def list_course_lessons(self, course_id: int) -> list[Lesson]:
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError('Course not found')
        return self.lesson_repository.list_by_course(course_id)

    def delete_lesson(self, lesson_id: int) -> None:
        lesson = self.lesson_repository.get_by_id(lesson_id)
        if lesson is None:
            raise ValueError('Lesson not found')
        return self.lesson_repository.delete(lesson)