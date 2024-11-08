from app.models import MealRequest  # Add this import

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def test_admin_crud_operations(client):
    # Admin login
    login(client, 'admin@example.com', 'adminpass')
    
    # Create a new meal request via admin
    response = client.post('/admin/add_request', data=dict(
        username='admin',
        email='admin@example.com',
        date='2023-10-12',
        breakfast=2,
        lunch=3,
        dinner=1
    ), follow_redirects=True)
    assert b'Meal request added successfully!' in response.data
    
    # Verify the new meal request appears in the dashboard
    response = client.get('/admin/dashboard')
    assert b'2023-10-12' in response.data
    assert b'2' in response.data  # Breakfast Quantity
    assert b'3' in response.data  # Lunch Quantity
    assert b'1' in response.data  # Dinner Quantity
    
    # Edit the meal request
    meal_request = MealRequest.query.filter_by(date='2023-10-12').first()
    assert meal_request is not None, "Meal request not found for the given date."
    response = client.post(f'/admin/edit_request/{meal_request.id}', data=dict(
        breakfast=3,
        lunch=4,
        dinner=2
    ), follow_redirects=True)
    assert b'Meal request updated successfully!' in response.data
    
    # Verify the updates
    response = client.get('/admin/dashboard')
    assert b'3' in response.data  # Updated Breakfast Quantity
    assert b'4' in response.data  # Updated Lunch Quantity
    assert b'2' in response.data  # Updated Dinner Quantity
    
    # Delete the meal request
    response = client.post(f'/admin/delete_request/{meal_request.id}', follow_redirects=True)
    assert b'Meal request deleted.' in response.data
    
    # Verify deletion
    response = client.get('/admin/dashboard')
    assert b'2023-10-12' not in response.data