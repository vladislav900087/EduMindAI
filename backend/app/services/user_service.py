from backend.app.core.security import hash_password
from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import UserCreate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user is not None:
            raise ValueError('A user with this email already exists')

        hashed_password = hash_password(user_data.password)

        user = User(email=user_data.email, hashed_password=hashed_password, full_name=user_data.full_name)

        return self.repository.create(user)