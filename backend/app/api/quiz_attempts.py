from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.security import get_current_user
from backend.app.api.dependencies import (get_quiz_attempt_service, get_quiz_questions_repository, get_quiz_for_management)
from backend.app.models.user import User, UserRole
from backend.app.schemas.quiz_attempt import (QuizAnswerRead, QuizAnswerSubmit, QuizAttemptRead, QuizAttemptStartRead, QuizTakingQuestionRead, QuizTakingOptionRead)
from backend.app.repositories.quiz_question_repository import QuizQuestionRepository

from backend.app.services.quiz_attempt_service import QuizAttemptService


router = APIRouter(tags=['Quiz Attempts'])

@router.post('/quizzes/{quiz_id}/attempts', response_model=QuizAttemptStartRead, status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(quiz_id: int, current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service), question_repository: QuizQuestionRepository = Depends(get_quiz_questions_repository)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can take quizzes')

    try:
        attempt = service.start_attempt(quiz_id=quiz_id, student_id=current_user.id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


    questions = question_repository.list_by_quiz(quiz_id)

    question_reads = []

    for question in questions:
        options = question_repository.list_options(question_id=question.id)

        question_reads.append(QuizTakingQuestionRead(id=question.id, question_text=question.question_text, options=[QuizTakingOptionRead(id=option.id, option_text=option.option_text) for option in options]))

    return QuizAttemptStartRead(attempt=attempt, questions=question_reads)

@router.post('/attempts/{attempt_id}/answers', response_model=QuizAnswerRead, status_code=status.HTTP_201_CREATED)
def submit_answer(attempt_id: int, answer_data: QuizAnswerSubmit, current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can answer quizzes')

    try:
        answer = service.submit_answer(student_id=current_user.id, attempt_id=attempt_id, question_id=answer_data.question_id, selected_option_id=answer_data.selected_option_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


    return answer

@router.post('/attempts/{attempt_id}/complete', response_model=QuizAttemptRead, status_code=status.HTTP_200_OK)
def complete_quiz_attempt(attempt_id: int, current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can complete quizzes')

    try:
        return service.complete_attempt(attempt_id=attempt_id, student_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get('/attempts/me', response_model=list[QuizAttemptRead], status_code=status.HTTP_200_OK)
def get_my_completed_attempts(current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can view quiz history')

    return service.list_completed_student_attempts(student_id=current_user.id)



@router.get('/attempts/{attempt_id}', response_model=QuizAttemptRead, status_code=status.HTTP_200_OK)
def get_quiz_attempt(attempt_id: int, current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only students can view quiz attempts')

    try:
        attempt = service.get_attempt(attempt_id)

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if attempt.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have access to this attempt')

    return attempt

@router.get('/quizzes/{quiz_id}/attempts', response_model=list[QuizAttemptRead], status_code=status.HTTP_200_OK)
def get_quiz_attempts(quiz_id: int, quiz=Depends(get_quiz_for_management), current_user: User = Depends(get_current_user), service: QuizAttemptService = Depends(get_quiz_attempt_service)):

    return service.list_quiz_attempts(quiz_id=quiz_id)





