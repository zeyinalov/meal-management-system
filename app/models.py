from flask_login import UserMixin
from datetime import datetime
from app import db  # Import db directly
from bcrypt import gensalt, hashpw, checkpw

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role

    def set_password(self, password):
        salt = gensalt()
        self.password_hash = hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_admin(self):
        return self.role.lower() == 'admin'

class MealRequest(db.Model):
    __tablename__ = 'meal_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    breakfast_quantity = db.Column(db.Integer, default=0)
    lunch_quantity = db.Column(db.Integer, default=0)
    dinner_quantity = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='meal_requests')

    def __init__(self, user_id, date, breakfast_quantity=0, lunch_quantity=0, dinner_quantity=0):
        self.user_id = user_id
        self.date = date
        self.breakfast_quantity = breakfast_quantity
        self.lunch_quantity = lunch_quantity
        self.dinner_quantity = dinner_quantity