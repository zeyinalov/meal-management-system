def test_403_error(client):
    # Log in as regular user
    login(client, 'user@example.com', 'userpass')
    # Attempt to access admin page
    response = client.get('/admin/dashboard')
    assert response.status_code == 403
    assert b'403 Forbidden' in response.data

def test_404_error(client):
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    assert b'404 Not Found' in response.data

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)