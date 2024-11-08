from flask import Blueprint, render_template, abort, Response, flash, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import MealRequest, User
from app import db
import openpyxl
from io import BytesIO
from datetime import datetime

admin = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to ensure the user has admin privileges."""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/admin/dashboard')
@admin_required
def dashboard():
    """Admin Dashboard displaying all meal requests."""
    meal_requests = MealRequest.query.order_by(MealRequest.timestamp.desc()).all()
    return render_template('admin/dashboard.html', meal_requests=meal_requests)

@admin.route('/admin/export-data')
@admin_required
def export_data():
    """Export meal request data to an Excel file."""
    meal_requests = MealRequest.query.order_by(MealRequest.timestamp.desc()).all()

    workbook = openpyxl.Workbook()
    sheet = workbook.create_sheet(title="Meal Requests")
    default_sheet = workbook['Sheet']
    workbook.remove(default_sheet)

    headers = ["Request ID", "Username", "Email", "Date", "Breakfast Quantity", "Lunch Quantity", "Dinner Quantity", "Timestamp"]
    sheet.append(headers)

    for request in meal_requests:
        row = [
            request.id,
            request.user.username,
            request.user.email,
            request.date.strftime('%Y-%m-%d'),
            request.breakfast_quantity,
            request.lunch_quantity,
            request.dinner_quantity,
            request.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ]
        sheet.append(row)

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    return Response(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=meal_requests.xlsx"}
    )

@admin.route('/admin/add_request', methods=['GET', 'POST'])
@admin_required
def add_request():
    """Add a new meal request."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        date_str = request.form.get('date', '').strip()
        breakfast = int(request.form.get('breakfast', 0))
        lunch = int(request.form.get('lunch', 0))
        dinner = int(request.form.get('dinner', 0))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User does not exist.', 'danger')
            return redirect(url_for('admin.add_request'))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('admin.add_request'))
        
        new_request = MealRequest(
            user_id=user.id,
            date=date,
            breakfast_quantity=breakfast,
            lunch_quantity=lunch,
            dinner_quantity=dinner
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Meal request added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_request.html')

@admin.route('/admin/edit_request/<int:request_id>', methods=['GET', 'POST'])
@admin_required
def edit_request(request_id):
    """Edit an existing meal request."""
    meal_request = MealRequest.query.get_or_404(request_id)
    if request.method == 'POST':
        meal_request.breakfast_quantity = int(request.form.get('breakfast', 0))
        meal_request.lunch_quantity = int(request.form.get('lunch', 0))
        meal_request.dinner_quantity = int(request.form.get('dinner', 0))
        db.session.commit()
        flash('Meal request updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_request.html', request=meal_request)

@admin.route('/admin/delete_request/<int:request_id>', methods=['POST'])
@admin_required
def delete_request(request_id):
    """Delete a meal request."""
    meal_request = MealRequest.query.get_or_404(request_id)
    db.session.delete(meal_request)
    db.session.commit()
    flash('Meal request deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
