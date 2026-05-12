from app.database import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # =========================
    # BASIC INFO
    # =========================
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # =========================
    # ROLE MANAGEMENT
    # =========================
    role = db.Column(db.String(20), nullable=False)  # employee / manager / hr

    # =========================
    # STATUS
    # =========================
    is_active = db.Column(db.Boolean, default=True)

    # =========================
    # TIMESTAMP
    # =========================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # RELATIONSHIPS (SAFE)
    # =========================

    # One-to-one profiles
    employee_profile = db.relationship(
        'Employee',
        backref='user',
        uselist=False,
        cascade="all, delete-orphan"
    )

    manager_profile = db.relationship(
        'Manager',
        backref='user',
        uselist=False,
        cascade="all, delete-orphan"
    )

    hr_profile = db.relationship(
        'HRAdmin',
        backref='user',
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Notifications
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Audit logs
    audit_logs = db.relationship(
        'AuditLog',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # =========================
    # FLASK-LOGIN REQUIRED
    # =========================
    def get_id(self):
        return str(self.id)

    # =========================
    # ROLE HELPERS
    # =========================
    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'

    def is_hr(self):
        return self.role == 'hr'

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"