from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.api.dependencies import get_current_user, get_assignment_service, get_assignment_for_management, get_course_for_management, get_submission_service, get_submission_for_management
from backend.app.schemas.assignment import AssignmentCreate, AssignmentRead
from backend.app.models.user import User, UserRole
from backend.app.services.assignment_service import AssignmentService
from backend.app.services.assignment_submission_service import AssignmentSubmissionService
from backend.app.schemas.assignment_submission import AssignmentSubmissionRead, AssignmentSubmissionCreate, AssignmentSubmissionGrade
from backend.app.utils.handle_service_error import handle_service_error




router = APIRouter(prefix='/assignments', tags=['Assignments'])
submission_router = APIRouter(prefix='/submissions', tags=['Assignment Submissions'])


@router.post('/courses/{course_id}', response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment(course_id: int, assignment_data: AssignmentCreate, course=Depends(get_course_for_management), current_user: User = Depends(get_current_user), service: AssignmentService = Depends(get_assignment_service)):
    try:
        return service.create_assignment(assignment_data=assignment_data, course_id=course_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

@router.post('/{assignment_id}/submissions', response_model=AssignmentSubmissionRead, status_code=status.HTTP_201_CREATED)
def submit_assignment(assignment_id: int, submission_data: AssignmentSubmissionCreate, current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):

    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can submit assignments')

    try:
        return service.create_submission(submission_data=submission_data, assignment_id=assignment_id, student_id=current_user.id)

    except ValueError as exc:
        raise handle_service_error(exc) from exc

@submission_router.get('/me', response_model=list[AssignmentSubmissionRead], status_code=status.HTTP_200_OK)
def list_my_submissions(current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):

    return service.list_student_submissions(student_id=current_user.id)


@submission_router.put('/{submission_id}', status_code=status.HTTP_200_OK, response_model=AssignmentSubmissionRead)
def update_submission(submission_id: int, submission_data: AssignmentSubmissionCreate, current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):
    try:
        submission = service.get_submission(submission_id=submission_id)
        if submission.student_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='This assignment submission does not belong to this student')

        return service.update_submission(assignment_id=submission.assignment_id, student_id=current_user.id, submission_data=submission_data)

    except ValueError as exc:
        raise handle_service_error(exc) from exc

@submission_router.put('/{submission_id}/grade', status_code=status.HTTP_200_OK, response_model=AssignmentSubmissionRead)
def grade_submission(submission_id: int, submission_data: AssignmentSubmissionGrade, submission=Depends(get_submission_for_management), current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):
    try:
        return service.grade_submission(submission=submission, grade=submission_data.grade, feedback=submission_data.feedback)

    except ValueError as exc:
        raise handle_service_error(exc) from exc




@submission_router.get('/{submission_id}', response_model=AssignmentSubmissionRead, status_code=status.HTTP_200_OK)
def get_submission(submission_id: int, current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):
    try:
        submission = service.get_submission(submission_id=submission_id)
        if submission.student_id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail='This assignment submission does not belong to this student')

        return submission
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc




@router.put('/{assignment_id}', status_code=status.HTTP_200_OK, response_model=AssignmentRead)
def update_assignment(assignment_id: int, assignment_data: AssignmentCreate, assignment=Depends(get_assignment_for_management), current_user: User = Depends(get_current_user), service: AssignmentService = Depends(get_assignment_service)):

    try:
        return service.update_assignment(assignment=assignment, assignment_data=assignment_data)

    except ValueError as exc:
        raise handle_service_error(exc) from exc


@router.get('/courses/{course_id}', response_model=list[AssignmentRead], status_code=status.HTTP_200_OK)
def list_assignments_by_course(course_id: int, current_user: User = Depends(get_current_user), service: AssignmentService = Depends(get_assignment_service)):

    try:
        return service.list_course_assignments(course_id=course_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get('/{assignment_id}', response_model=AssignmentRead, status_code=status.HTTP_200_OK)
def get_assignment(assignment_id: int, service: AssignmentService = Depends(get_assignment_service)):
    try:
        return service.get_assignment(assignment_id=assignment_id)
    except ValueError as exc:
        raise handle_service_error(exc) from exc

@router.get('/{assignment_id}/submissions', response_model=list[AssignmentSubmissionRead], status_code=status.HTTP_200_OK)
def list_students_submissions(assignment_id: int, assignment=Depends(get_assignment_for_management), current_user: User = Depends(get_current_user), service: AssignmentSubmissionService = Depends(get_submission_service)):
    try:
        return service.list_assignment_submissions(assignment_id=assignment_id)
    except ValueError as exc:
        raise handle_service_error(exc) from exc

@router.delete('/{assignment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, assignment=Depends(get_assignment_for_management), current_user: User = Depends(get_current_user), service: AssignmentService = Depends(get_assignment_service)):
    try:
        service.delete_assignment(assignment)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


