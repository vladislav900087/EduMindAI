import pytest
from pydantic import ValidationError

from backend.app.schemas.user import UserCreate

def test_user_create_accepts_valid_data():
    user = UserCreate(email='student@example.com', full_name='Test Student', password='password123')

    assert user.email == 'student@example.com'

def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email='student@example.com',
            full_name='Test Student',
            password='short'
        )

def test_user_create_rejects_empty_name():
    with pytest.raises(ValidationError):
        UserCreate(
            email='student@example.com',
            full_name='',
            password='password123'
        )

def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email='not-an-email',
            full_name='Test Student',
            password='password123'
        )