from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.router import router
from backend.app.core.config import settings
from backend.app.db.database import Base, engine
app = FastAPI(title=settings.app_name, description=settings.app_description, version=settings.app_version)

app.include_router(router)

origins = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173'
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=['*'])



@app.get('/')
def root():
    return {'message': 'Welcome to EduMind API!'}

