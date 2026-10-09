import pytest
from backend.app.repositories.user_repository import UserRepository
from backend.app.core.security import hash_password
from backend.app.models.user import User, UserRole, UserRegion, InterfaceLanguage
from backend.tests.test_quiz_attempt_api import create_test_user_and_login



def create_test_user(db_session, region: str, language: str) -> User:

    repository = UserRepository(db_session)

    return repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT, language=language, region=region))

def test_get_current_user(client):
    client.post('/auth/register', json={'email': 'current_user@example.com', 'password': 'StrongPassword123!', 'full_name': 'Current User'})

    login_response = client.post('/auth/login', data={'username': 'current_user@example.com', 'password': 'StrongPassword123!'})

    assert login_response.status_code == 200

    token = login_response.json()['access_token']

    response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    data = response.json()

    assert data['email'] == 'current_user@example.com'
    assert data['full_name'] == 'Current User'


def test_get_current_user_without_authentication(client):
    response = client.get('/users/me')

    assert response.status_code == 401

def test_new_user_defaults_to_kazakhstan_and_english(db_session, client):

    repository = UserRepository(db_session)


    new_user = repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT))

    assert new_user.region == 'kazakhstan'
    assert new_user.language == 'en'

def test_user_can_select_kazakhstan_and_russian(db_session, client):

    repository = UserRepository(db_session)

    user = repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT, region=UserRegion.KAZAKHSTAN.value, language=InterfaceLanguage.RUSSIAN.value))

    assert user is not None
    assert user.region == 'kazakhstan'
    assert user.language == 'ru'

def test_user_can_select_kazakhstan_and_kazakh(db_session, client):

    repository = UserRepository(db_session)

    user = repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT, region=UserRegion.KAZAKHSTAN.value, language=InterfaceLanguage.KAZAKH.value))

    assert user is not None
    assert user.region == 'kazakhstan'
    assert user.language == 'kk'

def test_user_can_select_europe_and_german(db_session, client):

    repository = UserRepository(db_session)

    user = repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT, region=UserRegion.EUROPE.value, language=InterfaceLanguage.GERMAN.value))

    assert User is not None
    assert user.region == 'europe'
    assert user.language == 'de'

def test_user_can_select_europe_and_english(db_session, client):

    repository = UserRepository(db_session)

    user = repository.create(User(email='random_user@example.com', full_name='Random User', hashed_password=hash_password('Password123!'), role=UserRole.STUDENT, region=UserRegion.EUROPE.value, language=InterfaceLanguage.ENGLISH.value))

    assert user is not None
    assert user.region == 'europe'
    assert user.language == 'en'

def test_user_cannot_select_europe_and_russian(db_session, client):

    payload = {
        'region': 'europe',
        'language': 'ru'
    }

    user_token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)

    response = client.patch('/users/me/preferences', json=payload, headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == 422

def test_user_cannot_select_europe_and_kazakh(db_session, client):

    payload = {
        'region': 'europe',
        'language': 'kk'
    }

    user_token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)
    response = client.patch('/users/me/preferences', json=payload, headers={"Authorization": f'Bearer {user_token}'})

    assert response.status_code == 422


def test_user_cannot_select_kazakhstan_and_german(db_session, client):

    payload = {
        'region': 'kazakhstan',
        'language': 'de'
    }

    user_token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)
    response = client.patch('/users/me/preferences', json=payload, headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == 422

def test_unauthenticated_user_returns_401(client):

    response = client.patch('/users/me/preferences')

    assert response.status_code == 401

def test_users_me_returns_saved_preferences(db_session, client):

    payload = {
        'region': 'europe',
        'language': 'de'
    }

    token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)

    update_response = client.patch('/users/me/preferences', json=payload, headers={'Authorization': f'Bearer {token}'})

    assert update_response.status_code == 200

    get_response = client.get('/users/me', headers={'Authorization': f'Bearer {token}'})

    assert get_response.status_code == 200
    assert get_response.json()['region'] == payload['region']
    assert get_response.json()['language'] == payload['language']


@pytest.mark.parametrize(
    ('region', 'language'),
    [
        ('kazakhstan', 'en'),
        ('kazakhstan', 'ru'),
        ('kazakhstan', 'kk'),
        ('europe', 'en'),
        ('europe', 'de')
    ],
)
def test_user_can_update_valid_preferences(db_session, client, region, language):

    token = create_test_user_and_login(db_session, client, role=UserRole.STUDENT)

    response = client.patch('/users/me/preferences', json={'region': region, 'language': language}, headers={"Authorization": f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['region'] == region
    assert response.json()['language'] == language











