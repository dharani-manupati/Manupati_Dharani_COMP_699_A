from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.auth_service import AuthService
from app.services.policy_service import PolicyService
from app.services.report_service import ReportService
from app.services.approval_service import ApprovalService
from app.services.notification_service import NotificationService

from app.models.user import User
from app.models.leave_policy import LeavePolicy
from app.models.leave_balance import LeaveBalance

hr_bp = Blueprint('hr', __name__)


# =========================
# DASHBOARD
# =========================
@hr_bp.route('/dashboard')
@login_required
def dashboard():

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    summary = ReportService.get_leave_summary()
    user_stats = ReportService.get_user_statistics()
    notifications = NotificationService.get_user_notifications(current_user.id, only_unread=True)

    return render_template(
        'hr/dashboard.html',
        summary=summary,
        user_stats=user_stats,
        notifications=notifications
    )


# =========================
# MANAGE USERS
# =========================
@hr_bp.route('/manage-users')
@login_required
def manage_users():

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    users = User.query.all()

    return render_template(
        'hr/manage_users.html',
        users=users
    )


# =========================
# ACTIVATE USER
# =========================
@hr_bp.route('/activate-user/<int:user_id>')
@login_required
def activate_user(user_id):

    success, message = AuthService.activate_user(user_id)

    flash(message, "success" if success else "error")
    return redirect(url_for('hr.manage_users'))


# =========================
# DEACTIVATE USER
# =========================
@hr_bp.route('/deactivate-user/<int:user_id>')
@login_required
def deactivate_user(user_id):

    success, message = AuthService.deactivate_user(user_id)

    flash(message, "success" if success else "error")
    return redirect(url_for('hr.manage_users'))


# =========================
# POLICIES LIST
# =========================
@hr_bp.route('/policies')
@login_required
def policies():

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    policies = LeavePolicy.query.all()

    return render_template(
        'hr/policies.html',
        policies=policies
    )


# =========================
# CREATE POLICY
# =========================
@hr_bp.route('/create-policy', methods=['GET', 'POST'])
@login_required
def create_policy():

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = {
            "policy_name": request.form.get('policy_name'),
            "leave_type": request.form.get('leave_type'),
            "max_days_per_year": int(request.form.get('max_days_per_year')),
            "max_days_per_request": int(request.form.get('max_days_per_request')),
            "carry_forward": bool(request.form.get('carry_forward')),
            "carry_forward_limit": int(request.form.get('carry_forward_limit') or 0),
            "requires_approval": bool(request.form.get('requires_approval')),
            "allow_half_day": bool(request.form.get('allow_half_day')),
            "min_days_notice": int(request.form.get('min_days_notice') or 0),
            "max_consecutive_days": int(request.form.get('max_consecutive_days') or 0)
        }

        success, message = PolicyService.create_policy(data, current_user.id)

        flash(message, "success" if success else "error")
        return redirect(url_for('hr.policies'))

    return render_template('hr/policies.html')


# =========================
# ASSIGN POLICY TO ALL
# =========================
@hr_bp.route('/assign-policy/<int:policy_id>')
@login_required
def assign_policy(policy_id):

    success, message = PolicyService.assign_policy_to_all_employees(policy_id, current_user.id)

    flash(message, "success" if success else "error")
    return redirect(url_for('hr.policies'))


# =========================
# REPORTS
# =========================
@hr_bp.route('/reports')
@login_required
def reports():

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    summary = ReportService.get_leave_summary()
    department_report = ReportService.get_department_report()
    balance_report = ReportService.get_leave_balance_report()

    return render_template(
        'hr/reports.html',
        summary=summary,
        department_report=department_report,
        balance_report=balance_report
    )


# =========================
# HR OVERRIDE
# =========================
@hr_bp.route('/override/<int:leave_id>', methods=['POST'])
@login_required
def override_leave(leave_id):

    if current_user.role != 'hr':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    comments = request.form.get('comments')

    success, message = ApprovalService.hr_override(
        current_user.id,
        leave_id,
        comments
    )

    flash(message, "success" if success else "error")
    return redirect(url_for('hr.dashboard'))