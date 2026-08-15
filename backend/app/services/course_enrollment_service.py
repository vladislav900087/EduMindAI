from backend.app.models.course_enrollment import CourseEnrollment
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.repositories.course_repository import CourseRepository

class CourseEnrollmentService:
    def __init__(self, enrollment_repository: CourseEnrollmentRepository, course_repository: CourseRepository):
        self.enrollment_repository = enrollment_repository
        self.course_repository = course_repository

    def enroll(self, student_id: int, course_id: int) -> CourseEnrollment:
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError('Course not found')

        existing_enrollment = self.enrollment_repository.get_by_student_and_course(student_id=student_id, course_id=course_id)
        if existing_enrollment is not None:
            raise ValueError('Student is already enrolled')

        enrollment = CourseEnrollment(student_id=student_id, course_id=course_id)

        return self.enrollment_repository.create(enrollment)

    def list_student_enrollments(self, student_id: int) -> list[CourseEnrollment]:
        return self.enrollment_repository.list_by_student(student_id)

    def list_course_enrollments(self, course_id: int) -> list[CourseEnrollment]:
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError('Course not found')
        return self.enrollment_repository.list_by_course(course_id)

    def unenroll(self, student_id: int, course_id: int) -> None:
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError('Course not found')

        current_enrollment = self.enrollment_repository.get_by_student_and_course(student_id=student_id, course_id=course_id)
        if current_enrollment is None:
            raise ValueError('Enrollment not found')

        return self.enrollment_repository.delete(current_enrollment)
