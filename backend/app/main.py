from fastapi import FastAPI
from backend.app.api.router import router

app = FastAPI(title='EduMind API', description='AI-powered Learning Management System', version='0.1.0')

app.include_router(router)

@app.get('/')
def root():
    return {'message': 'Welcome to EduMind API!'}

