from app.models import User, MealRequest
from app import db

from io import BytesIO
import openpyxl

def test_export_data(client):
    with client.application.app_context():
        # Create admin user and meal requests
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(username='admin2', email='admin2@example.com', role='admin')
            admin_user.set_password('admin2pass')
            db.session.add(admin_user)
            db.session.commit()
        
        meal1 = MealRequest(user_id=admin_user.id, date='2023-10-12', breakfast_quantity=2, lunch_quantity=3, dinner_quantity=1)
        db.session.add(meal1)
        db.session.commit()
    
    # Admin login
    login(client, 'admin2@example.com', 'admin2pass')
    response = client.get('/admin/export-data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert 'attachment;filename=meal_requests.xlsx' in response.headers['Content-Disposition']
    
    # Verify Excel content
    workbook = openpyxl.load_workbook(filename=BytesIO(response.data))
    sheet = workbook['Meal Requests']
    # Check headers
    headers = [cell.value for cell in sheet[1]]
    assert headers == ["Request ID", "Username", "Email", "Date", "Breakfast Quantity", "Lunch Quantity", "Dinner Quantity", "Timestamp"]
    # Check data
    data_rows = list(sheet.iter_rows(min_row=2, values_only=True))
    assert len(data_rows) == 1
    assert data_rows[0][3] == '2023-10-12'  # Date
    assert data_rows[0][4] == 2  # Breakfast Quantity
    assert data_rows[0][5] == 3  # Lunch Quantity
    assert data_rows[0][6] == 1  # Dinner Quantity

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)