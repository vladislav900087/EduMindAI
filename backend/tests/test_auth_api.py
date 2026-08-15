

def test_auth_api(client):
    response = client.post('/auth/register', json={"email": 'api_test@example.com', 'password': 'StrongPassword123!', 'full_name': 'API Test User'})

    assert response.status_code == 201

    data = response.json()

    assert data['email'] == 'api_test@example.com'
    assert data['full_name'] == 'API Test User'
    assert 'id' in data

def test_register_duplicate_email(client):
    user_data = {
        'email': 'duplicate@example.com',
        'password': 'StrongPassword123!',
        'full_name': 'Duplicate User'
    }

    first_response = client.post('auth/register', json=user_data)

    assert first_response.status_code == 201

    second_response = client.post('auth/register', json=user_data)

    assert second_response.status_code == 400

def test_login_user(client):
    client.post('/auth/register', json={'email': 'login@example.com', 'password': 'StrongPassword123!', 'full_name': 'Login User'})

    response = client.post('/auth/login', data={'username': 'login@example.com', 'password': 'StrongPassword123!'})

    assert response.status_code == 200

    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

def test_login_invalid_password(client):
    client.post('/auth/register', json={'email': 'wrong_password@example.com', 'password': 'CorrectPassword123!', 'full_name': 'Wrong Password User'})

    response = client.post('/auth/login', data={'username': 'wrong_password@example.com', 'password': 'WrongPassword123!'})

    assert response.status_code == 401
