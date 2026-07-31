from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import UserCreate, UserRead, UserLogin, Token
from backend.app.services.user_service import UserService

from backend.app.api.dependencies import get_user_service

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = service.create_user(user_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return user

@router.post('/login', response_model=Token)
def login(credentials: UserLogin, service: UserService = Depends(get_user_service)):
    try:
        token = service.login(credentials.email, credentials.password)

        return {
            'access_token': token,
            'token_type': 'bearer'
        }

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


