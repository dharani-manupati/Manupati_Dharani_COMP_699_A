from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.auth_service import AuthService
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


# =========================
# REGISTER
# =========================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        data = {
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "role": request.form.get('role'),
            "full_name": request.form.get('full_name'),
            "department": request.form.get('department'),
            "designation": request.form.get('designation')
        }

        success, message = AuthService.register_user(data)

        if success:
            flash(message, "success")
            return redirect(url_for('auth.login'))
        else:
            flash(message, "error")

    return render_template('auth/register.html')


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user, message = AuthService.login_user(username, password)

        if user:
            login_user(user)
            flash(message, "success")

            # Role-based redirect
            if user.role == 'employee':
                return redirect(url_for('employee.dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('manager.dashboard'))
            elif user.role == 'hr':
                return redirect(url_for('hr.dashboard'))

        else:
            flash(message, "error")

    return render_template('auth/login.html')


# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))


# =========================
# REDIRECT BASED ON ROLE
# =========================
@auth_bp.route('/redirect')
@login_required
def redirect_dashboard():

    if current_user.role == 'employee':
        return redirect(url_for('employee.dashboard'))

    elif current_user.role == 'manager':
        return redirect(url_for('manager.dashboard'))

    elif current_user.role == 'hr':
        return redirect(url_for('hr.dashboard'))

    return redirect(url_for('auth.login'))