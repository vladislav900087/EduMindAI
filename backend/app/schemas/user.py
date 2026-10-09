from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from backend.app.models.user import UserRole, UserRegion, InterfaceLanguage


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserRead(UserBase):
    id: int
    role: UserRole
    region: UserRegion
    language: InterfaceLanguage
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPreferencesUpdate(BaseModel):
    region: UserRegion
    language: InterfaceLanguage

    @model_validator(mode='after')
    def validate_region_language(self):
        allowed_languages = {
            UserRegion.KAZAKHSTAN: {
                InterfaceLanguage.ENGLISH,
                InterfaceLanguage.RUSSIAN,
                InterfaceLanguage.KAZAKH,
            },
            UserRegion.EUROPE: {
                InterfaceLanguage.ENGLISH,
                InterfaceLanguage.GERMAN
            },
        }

        if self.language not in allowed_languages[self.region]:
            raise ValueError('Selected language is not available in this region')

        return self



