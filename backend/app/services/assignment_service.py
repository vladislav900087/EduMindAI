from backend.app.models.assignment import Assignment
from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.course_repository import CourseRepository
from backend.app.schemas.assignment import AssignmentCreate

class AssignmentService:
    def __init__(self, repository: AssignmentRepository, course_repository: CourseRepository):
        self.repository = repository
        self.course_repository = course_repository

    def create_assignment(self, assignment_data: AssignmentCreate, course_id: int) -> Assignment:
        course = self.course_repository.get_by_id(course_id)

        if course is None:
            raise ValueError('Course not found')

        assignment = Assignment(title=assignment_data.title, description=assignment_data.description, course_id=course_id, due_at=assignment_data.due_at)

        return self.repository.create(assignment)

    def get_assignment(self, assignment_id: int) -> Assignment:

        assignment = self.repository.get_by_id(assignment_id)

        if assignment is None:
            raise ValueError('Assignment not found')

        return assignment

    def list_course_assignments(self, course_id: int) -> list[Assignment]:
        course = self.course_repository.get_by_id(course_id)

        if course is None:
            raise ValueError('Course not found')

        return self.repository.list_by_course(course_id)

    def update_assignment(self, assignment: Assignment, assignment_data: AssignmentCreate) -> Assignment:
        assignment.title = assignment_data.title
        assignment.description = assignment_data.description
        assignment.due_at = assignment_data.due_at

        return self.repository.update(assignment)

    def delete_assignment(self, assignment: Assignment) -> None:
        self.repository.delete(assignment)



