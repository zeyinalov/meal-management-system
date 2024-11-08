def test_login_logout(client):
    # Register a new user
    response = client.post('/register', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='testpass',
        role='user'
    ), follow_redirects=True)
    assert b'Registration successful!' in response.data
    
    # Login with the new user
    response = login(client, 'testuser@example.com', 'testpass')
    assert b'Logged in successfully!' in response.data
    
    # Access protected route
    response = client.get('/view_requests')
    assert response.status_code == 200
    assert b'My Meal Requests' in response.data
    
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b'Logged out successfully!' in response.data
    
    # Access protected route after logout
    response = client.get('/view_requests', follow_redirects=True)
    assert b'Please log in to access this page.' in response.data

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)