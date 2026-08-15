
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
