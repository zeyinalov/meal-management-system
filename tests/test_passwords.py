from app.models import User
from app import db

def test_password_hashing(client):
    with client.application.app_context():
        user = User(username='hashuser', email='hashuser@example.com', role='user')
        user.set_password('securepassword')
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.filter_by(email='hashuser@example.com').first()
        assert retrieved_user is not None
        assert retrieved_user.password_hash != 'securepassword'
        assert retrieved_user.check_password('securepassword') is True
        assert retrieved_user.check_password('wrongpassword') is False