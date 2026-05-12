from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.services.approval_service import ApprovalService
from app.services.notification_service import NotificationService
from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.models.manager import Manager

manager_bp = Blueprint('manager', __name__)


# =========================
# DASHBOARD
# =========================
@manager_bp.route('/dashboard')
@login_required
def dashboard():

    if current_user.role != 'manager':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    manager = Manager.query.filter_by(user_id=current_user.id).first()

    if not manager:
        flash("Manager profile not found", "error")
        return redirect(url_for('auth.login'))

    # Team members
    team = Employee.query.filter_by(manager_id=manager.id).all()

    # Pending requests
    pending_requests = LeaveRequest.query.filter_by(
        manager_id=manager.id,
        status='pending'
    ).order_by(LeaveRequest.created_at.desc()).all()

    notifications = NotificationService.get_user_notifications(
        current_user.id,
        only_unread=True
    )

    return render_template(
        'manager/dashboard.html',
        manager=manager,
        team=team,
        pending_requests=pending_requests,
        notifications=notifications
    )


# =========================
# REVIEW REQUESTS
# =========================
@manager_bp.route('/review-requests')
@login_required
def review_requests():

    if current_user.role != 'manager':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    manager = Manager.query.filter_by(user_id=current_user.id).first()

    if not manager:
        flash("Manager profile not found", "error")
        return redirect(url_for('auth.login'))

    requests = LeaveRequest.query.filter_by(
        manager_id=manager.id
    ).order_by(
        LeaveRequest.created_at.desc()   # ✅ FIXED HERE
    ).all()

    return render_template(
        'manager/review_requests.html',
        requests=requests
    )


# =========================
# APPROVE LEAVE
# =========================
@manager_bp.route('/approve/<int:leave_id>', methods=['POST'])
@login_required
def approve_leave(leave_id):

    if current_user.role != 'manager':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    comments = request.form.get('comments')

    success, message = ApprovalService.approve_leave(
        current_user.id,
        leave_id,
        comments
    )

    flash(message, "success" if success else "error")

    return redirect(url_for('manager.review_requests'))


# =========================
# REJECT LEAVE
# =========================
@manager_bp.route('/reject/<int:leave_id>', methods=['POST'])
@login_required
def reject_leave(leave_id):

    if current_user.role != 'manager':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    comments = request.form.get('comments')

    success, message = ApprovalService.reject_leave(
        current_user.id,
        leave_id,
        comments
    )

    flash(message, "success" if success else "error")

    return redirect(url_for('manager.review_requests'))


# =========================
# TEAM HISTORY
# =========================
@manager_bp.route('/team-history')
@login_required
def team_history():

    if current_user.role != 'manager':
        flash("Unauthorized access", "error")
        return redirect(url_for('auth.login'))

    manager = Manager.query.filter_by(user_id=current_user.id).first()

    if not manager:
        flash("Manager profile not found", "error")
        return redirect(url_for('auth.login'))

    # ✅ FIXED: directly fetch using manager_id
    team_leaves = LeaveRequest.query.filter_by(
        manager_id=manager.id
    ).order_by(
        LeaveRequest.created_at.desc()
    ).all()

    return render_template(
        'manager/team_history.html',
        team_leaves=team_leaves
    )