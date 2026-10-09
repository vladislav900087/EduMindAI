from fastapi import APIRouter, Depends

from backend.app.api.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserRead, UserPreferencesUpdate
from backend.app.api.dependencies import get_user_service
from backend.app.services.user_service import UserService


from backend.app.api.authorization import require_roles
from backend.app.models.user import UserRole


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch('/me/preferences', response_model=UserRead)
def update_my_preferences(preferences: UserPreferencesUpdate, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)):

    return service.update_preferences(
        user=current_user,
        preferences=preferences
    )



