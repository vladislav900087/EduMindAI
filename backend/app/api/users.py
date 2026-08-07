from fastapi import APIRouter, Depends

from backend.app.api.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserRead

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

