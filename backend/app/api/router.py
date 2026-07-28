from fastapi import APIRouter
from backend.app.api.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)

@router.get('/health')
def health_check():
    return {'status': 'ok'}