from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from typing import Optional, Union
from app.models import User
from app import db, bcrypt
from werkzeug.wrappers import Response

auth = Blueprint('auth', __name__)

# Load user function for Flask-Login
from app import login_manager

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register() -> Union[str, Response]:
    if request.method == 'POST':
        # Capture form data
        username: str = request.form.get('username', '').strip()
        email: str = request.form.get('email', '').strip()
        password: str = request.form.get('password', '').strip()
        role: str = request.form.get('role', '').strip()  # Ensure 'role' is valid if using role-based access control

        if not all([username, email, password, role]):
            flash('Please fill out all fields!', 'warning')
            return redirect(url_for('auth.register'))

        # Check if the user already exists
        existing_user: Optional[User] = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered!', 'warning')
            return redirect(url_for('auth.register'))

        # Create and add the new user to the database
        user: User = User(username=username, email=email, role=role)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Response]:
    if request.method == 'POST':
        # Capture form data
        email: str = request.form.get('email', '').strip()
        password: str = request.form.get('password', '').strip()

        if not all([email, password]):
            flash('Please enter both email and password.', 'warning')
            return redirect(url_for('auth.login'))

        # Check if the user exists
        user: Optional[User] = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/')
def home() -> Union[str, Response]:
    return "Welcome to the Meal Management System!"
