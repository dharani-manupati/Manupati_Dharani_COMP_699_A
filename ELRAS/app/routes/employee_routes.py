from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.leave_service import LeaveService
from app.services.notification_service import NotificationService
from app.models.employee import Employee
from app.models.leave_balance import LeaveBalance

employee_bp = Blueprint('employee', __name__)


# =========================
# DASHBOARD
# =========================
@employee_bp.route('/dashboard')
@login_required
def dashboard():

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    employee = Employee.query.filter_by(user_id=current_user.id).first()

    balances = LeaveBalance.query.filter_by(employee_id=employee.id).all()

    notifications = NotificationService.get_user_notifications(current_user.id, only_unread=True)

    return render_template(
        'employee/dashboard.html',
        employee=employee,
        balances=balances,
        notifications=notifications
    )


# =========================
# APPLY LEAVE
# =========================
@employee_bp.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = {
            "leave_type": request.form.get('leave_type'),
            "start_date": request.form.get('start_date'),
            "end_date": request.form.get('end_date'),
            "reason": request.form.get('reason')
        }

        file = request.files.get('document')

        success, message = LeaveService.apply_leave(current_user.id, data, file)

        if success:
            flash(message, "success")
            return redirect(url_for('employee.leave_history'))
        else:
            flash(message, "error")

    return render_template('employee/apply_leave.html')


# =========================
# LEAVE HISTORY
# =========================
@employee_bp.route('/leave-history')
@login_required
def leave_history():

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    leaves = LeaveService.get_user_leaves(current_user.id)

    return render_template(
        'employee/leave_history.html',
        leaves=leaves
    )


# =========================
# CANCEL LEAVE
# =========================
@employee_bp.route('/cancel-leave/<int:leave_id>')
@login_required
def cancel_leave(leave_id):

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    success, message = LeaveService.cancel_leave(current_user.id, leave_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for('employee.leave_history'))


# =========================
# LEAVE BALANCE
# =========================
@employee_bp.route('/leave-balance')
@login_required
def leave_balance():

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    employee = Employee.query.filter_by(user_id=current_user.id).first()

    balances = LeaveBalance.query.filter_by(employee_id=employee.id).all()

    return render_template(
        'employee/leave_balance.html',
        balances=balances
    )


# =========================
# PROFILE
# =========================
@employee_bp.route('/profile')
@login_required
def profile():

    if current_user.role != 'employee':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    employee = Employee.query.filter_by(user_id=current_user.id).first()

    return render_template(
        'employee/profile.html',
        employee=employee
    )