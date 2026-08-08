from fastapi import APIRouter, Depends

from backend.app.api.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserRead

from backend.app.api.authorization import require_roles
from backend.app.models.user import UserRole


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/admin-test')
def admin_test(current_user: User = Depends(require_roles(UserRole.ADMIN))):
    return {
        'message': 'You have administrator access.',
        'user_id': current_user.id
    }
