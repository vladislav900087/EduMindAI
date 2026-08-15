from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.course_enrollment import CourseEnrollment

class CourseEnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, enrollment: CourseEnrollment) -> CourseEnrollment:
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

        return enrollment

    def get_by_id(self, enrollment_id: int) -> CourseEnrollment | None:
        statement = select(CourseEnrollment).where(CourseEnrollment.id == enrollment_id)

        return self.db.scalar(statement)

    def get_by_student_and_course(self, student_id: int, course_id: int) -> CourseEnrollment | None:
        statement = select(CourseEnrollment).where(CourseEnrollment.student_id == student_id, CourseEnrollment.course_id == course_id)

        return self.db.scalar(statement)

    def list_by_student(self, student_id: int) -> list[CourseEnrollment]:
        statement = select(CourseEnrollment).where(CourseEnrollment.student_id == student_id)

        return list(self.db.scalars(statement))

    def list_by_course(self, course_id: int) -> list[CourseEnrollment]:
        statement = select(CourseEnrollment).where(CourseEnrollment.course_id == course_id)

        return list(self.db.scalars(statement))

    def delete(self, enrollment: CourseEnrollment) -> None:
        self.db.delete(enrollment)
        self.db.commit()
