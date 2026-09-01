from backend.app.repositories.assignment_repository import AssignmentRepository
from backend.app.repositories.assignment_submission_repository import AssignmentSubmissionRepository
from backend.app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from backend.app.schemas.assignment_submission import AssignmentSubmissionCreate
from backend.app.models.assignment_submission import AssignmentSubmission
from datetime import datetime, timezone
import logging



from backend.app.tasks.notifications import send_assignment_graded_notification


logger = logging.getLogger(__name__)



class AssignmentSubmissionService:
    def __init__(self, submission_repository: AssignmentSubmissionRepository, enrollment_repository: CourseEnrollmentRepository, assignment_repository: AssignmentRepository):
        self.submission_repository = submission_repository
        self.enrollment_repository = enrollment_repository
        self.assignment_repository = assignment_repository


    def create_submission(self, submission_data: AssignmentSubmissionCreate, assignment_id: int, student_id: int) -> AssignmentSubmission:
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if assignment is None:
            raise ValueError('Assignment not found')

        if assignment.due_at is not None and assignment.due_at < datetime.now(timezone.utc):
            raise ValueError('Assignment has expired')

        student_enrollment = self.enrollment_repository.get_by_student_and_course(course_id=assignment.course_id, student_id=student_id)
        if student_enrollment is None:
            raise ValueError('Student is not enrolled to this course')

        existing_submission = self.submission_repository.get_by_student_and_assignment(student_id=student_id, assignment_id=assignment.id)
        if existing_submission is not None:
            raise ValueError('This assignment is already submitted')

        submission = self.submission_repository.create(AssignmentSubmission(student_id=student_id, assignment_id=assignment.id, content=submission_data.content))

        return submission

    def get_submission(self, submission_id: int) -> AssignmentSubmission:
        submission = self.submission_repository.get_by_id(submission_id)

        if submission is None:
            raise ValueError('Submission not found')

        return submission

    def list_student_submissions(self, student_id: int) -> list[AssignmentSubmission]:
        return self.submission_repository.list_by_student(student_id=student_id)

    def list_assignment_submissions(self, assignment_id: int) -> list[AssignmentSubmission]:
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if assignment is None:
            raise ValueError('Assignment not found')
        return self.submission_repository.list_by_assignment(assignment_id=assignment_id)

    def update_submission(self, assignment_id: int, student_id: int, submission_data: AssignmentSubmissionCreate) -> AssignmentSubmission:
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if assignment is None:
            raise ValueError('Assignment not found')

        if assignment.due_at is not None and assignment.due_at < datetime.now(timezone.utc):
            raise ValueError('Assignment has expired')

        submission = self.submission_repository.get_by_student_and_assignment(student_id=student_id, assignment_id=assignment.id)
        if submission is None:
            raise ValueError('Submission not found')

        if submission.grade is not None:
            raise ValueError('This assignment has already been graded')

        submission.content = submission_data.content
        submission.updated_at = datetime.now(timezone.utc)

        return self.submission_repository.update(submission)

    def grade_submission(self, submission: AssignmentSubmission, grade: int, feedback: str | None = None) -> AssignmentSubmission:


        if submission is None:
            raise ValueError('Submission is not specified')

        if submission.grade is not None and submission.graded_at is not None:
            raise ValueError('This submission has already been graded')

        if grade is None:
            raise ValueError('Grade is not specified')

        if 0 <= grade <= 100:
            submission.grade = grade
            submission.graded_at = datetime.now(timezone.utc)
            if feedback is not None:
                submission.feedback = feedback

            graded_submission = self.submission_repository.update(submission)
            try:

                task = send_assignment_graded_notification.delay(student_email=submission.student.email,
                                                          assignment_title=submission.assignment.title, grade=grade,
                                                          feedback=feedback)

                logger.info('Assignment notification queued %s', task.id)

            except Exception as exc:
                logger.error(f'Failed to queue graded notification task {exc}')



            return graded_submission
        else:
            raise ValueError('Grade must be between 0 and 100')











