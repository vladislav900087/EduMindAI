from backend.app.models.lesson_progress import LessonProgress
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.lesson_progress_repository import LessonProgressRepository
from backend.app.repositories.lesson_repository import LessonRepository
from backend.app.repositories.course_repository import CourseRepository


class LessonProgressService:
    def __init__(self, progress_repository: LessonProgressRepository, enrollment_repository: CourseEnrollmentRepository, lesson_repository: LessonRepository, course_repository: CourseRepository):
        self.progress_repository = progress_repository
        self.enrollment_repository = enrollment_repository
        self.lesson_repository = lesson_repository
        self.course_repository = course_repository

    def mark_lesson_complete(self, student_id: int, lesson_id: int) -> LessonProgress:
        lesson = self.lesson_repository.get_by_id(lesson_id)
        if lesson is None:
            raise ValueError('Lesson not found')

        course_id = lesson.course_id

        enrollment = self.enrollment_repository.get_by_student_and_course(student_id=student_id, course_id=course_id)

        if enrollment is None:
            raise ValueError('Student is not enrolled in this course')

        existing_progress = self.progress_repository.get_by_student_and_lesson(student_id, lesson_id)

        if existing_progress is not None:
            raise ValueError('Lesson is already completed')

        progress = LessonProgress(student_id=student_id, lesson_id=lesson_id)

        return self.progress_repository.create(progress)

    def list_student_progress(self, student_id: int) -> list[LessonProgress]:
        return self.progress_repository.list_by_student(student_id)

    def get_course_progress(self, student_id: int, course_id: int) -> dict:

        course = self.course_repository.get_by_id(course_id)

        if course is None:
            raise ValueError('Course not found')

        enrollment = self.enrollment_repository.get_by_student_and_course(student_id, course_id)

        if enrollment is None:
            raise ValueError('Student is not enrolled in this course')

        lessons = self.lesson_repository.list_by_course(course_id)

        total_lessons = len(lessons)

        completed_progress = self.progress_repository.list_by_student_and_course(student_id=student_id, course_id=course_id)

        completed_lessons = len(completed_progress)

        progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0.0

        return {
            'course_id': course_id,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': progress_percentage
        }
