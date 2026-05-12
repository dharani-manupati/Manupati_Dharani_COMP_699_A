from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.notification_service import NotificationService

common_bp = Blueprint('common', __name__)


# =========================
# HOME PAGE (UPDATED)
# =========================
@common_bp.route('/')
def home():
    """
    Redirect to login or dashboard
    """
    if current_user.is_authenticated:
        return redirect(url_for('auth.redirect_dashboard'))

    # 🔥 FIX: directly go to login page
    return redirect(url_for('auth.login'))


# =========================
# ALL NOTIFICATIONS
# =========================
@common_bp.route('/notifications')
@login_required
def notifications():

    notifications = NotificationService.get_user_notifications(current_user.id)

    return render_template(
        'common/notifications.html',
        notifications=notifications
    )


# =========================
# MARK SINGLE AS READ
# =========================
@common_bp.route('/notifications/read/<int:notification_id>')
@login_required
def mark_read(notification_id):

    success, message = NotificationService.mark_as_read(notification_id)

    if not success:
        flash(message, "error")

    return redirect(url_for('common.notifications'))


# =========================
# MARK ALL AS READ
# =========================
@common_bp.route('/notifications/read-all')
@login_required
def mark_all_read():

    NotificationService.mark_all_as_read(current_user.id)

    flash("All notifications marked as read", "success")
    return redirect(url_for('common.notifications'))