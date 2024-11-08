from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from typing import Optional, Union
from app.models import MealRequest
from app import db
from werkzeug.wrappers import Response

meal = Blueprint('meal', __name__)

@meal.route('/submit_request', methods=['GET', 'POST'])
@login_required
def submit_request() -> Union[str, Response]:
    if request.method == 'POST':
        current_time = datetime.now().time()
        start_time = datetime.strptime('08:00', '%H:%M').time()
        end_time = datetime.strptime('11:00', '%H:%M').time()
        
        if not (start_time <= current_time <= end_time):
            flash("Requests can only be submitted between 8 and 11 AM.", 'warning')
            return redirect(url_for('meal.submit_request'))

        date_str: str = request.form.get('date', '').strip()
        if not date_str:
            flash("Date is required.", 'warning')
            return redirect(url_for('meal.submit_request'))
        
        try:
            date: datetime = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", 'danger')
            return redirect(url_for('meal.submit_request'))

        try:
            breakfast = int(request.form.get('breakfast', 0))
            lunch = int(request.form.get('lunch', 0))
            dinner = int(request.form.get('dinner', 0))
        except ValueError:
            flash("Invalid input for meal quantities. Please enter integers.", 'danger')
            return redirect(url_for('meal.submit_request'))

        new_request = MealRequest(
            user_id=current_user.id,
            date=date,
            breakfast_quantity=breakfast,
            lunch_quantity=lunch,
            dinner_quantity=dinner
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Meal request submitted successfully!', 'success')
        return redirect(url_for('meal.view_requests'))

    return render_template('submit_request.html')

@meal.route('/view_requests')
@login_required
def view_requests() -> str:
    requests = MealRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('view_requests.html', requests=requests)