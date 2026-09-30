from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from backend.app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserRead(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

