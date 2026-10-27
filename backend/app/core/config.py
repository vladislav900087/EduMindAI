from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BACKEND_DIR / ".env"



class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_description: str

    database_url: str
    test_database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    celery_broker_url: str

    smtp_host: str = 'smtp.gmail.com'
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from_email: str
    smtp_tls: bool = True

    gemini_api_key: str = ''
    gemini_model: str = 'gemini-3.1-flash-lite'


    environment: Literal['development', 'test', 'production'] = 'development'
    payment_provider: str = 'disabled'



    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        extra='ignore'

    )



settings = Settings()