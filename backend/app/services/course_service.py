from backend.app.models.course import Course, CourseStatus
from backend.app.models.user import User
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.course import CourseCreate

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def create_course(self, course_data: CourseCreate, teacher: User) -> Course:
        course = Course(title=course_data.title, description=course_data.description, teacher_id=teacher.id)

        return self.repository.create(course)

    def publish_course(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)

        if course is None:
            raise ValueError('Course not found')

        if course.status != CourseStatus.DRAFT:
            raise ValueError('Only draft courses can be published')

        course.status = CourseStatus.PUBLISHED

        return self.repository.update(course)

    def get_course(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)

        if course is None:
            raise ValueError('Course not found')

        return course

    def list_courses(self) -> list[Course]:
        return self.repository.list_all()

    def list_teacher_courses(self, teacher_id: int) -> list[Course]:
        return self.repository.list_by_teacher(teacher_id)