

def test_auth_api(client):
    response = client.post('/auth/register', json={"email": 'api_test@example.com', 'password': 'StrongPassword123!', 'full_name': 'API Test User'})

    assert response.status_code == 201

    data = response.json()

    assert data['email'] == 'api_test@example.com'
    assert data['full_name'] == 'API Test User'
    assert 'id' in data