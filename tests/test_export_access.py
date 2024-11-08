def test_export_access_control(client):
    # Regular user login
    login(client, 'user@example.com', 'userpass')
    response = client.get('/admin/export-data')
    assert response.status_code == 403
    assert b'403 Forbidden' in response.data


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)