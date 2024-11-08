from app.models import User, MealRequest  # Import User and MealRequest models
from app import db  # Import the db instance

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def test_admin_dashboard_data(client):
    with client.application.app_context():
        # Ensure the admin user exists
        user = User.query.filter_by(email='admin@example.com').first()
        if not user:
            user = User(username='admin', email='admin@example.com', role='admin')
            user.set_password('adminpass')
            db.session.add(user)
            db.session.commit()

        # Create meal requests
        meal1 = MealRequest(user_id=user.id, date='2023-10-10', breakfast_quantity=1, lunch_quantity=2, dinner_quantity=3)
        meal2 = MealRequest(user_id=user.id, date='2023-10-11', breakfast_quantity=0, lunch_quantity=1, dinner_quantity=1)
        db.session.add_all([meal1, meal2])
        db.session.commit()

    # Admin login
    login(client, 'admin@example.com', 'adminpass')
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Meal Requests' in response.data
    assert b'2023-10-10' in response.data
    assert b'2023-10-11' in response.data
    assert b'1' in response.data  # Breakfast Quantity for meal1
    assert b'2' in response.data  # Lunch Quantity for meal1
    assert b'3' in response.data  # Dinner Quantity for meal1