from app.database import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)

    # Link to User (login account)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    # Employee Details
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    # Work Details
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)

    # Reporting Manager
    manager_id = db.Column(
        db.Integer,
        db.ForeignKey('managers.id'),
        nullable=True
    )

    # Employment Info
    join_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active / inactive

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # RELATIONSHIPS (SAFE)
    # =========================

    # Leave balances of employee
    leave_balances = db.relationship(
        'LeaveBalance',
        backref='employee',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Uploaded documents
    documents = db.relationship(
        'Document',
        backref='employee',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Leave requests (IMPORTANT for templates)
    leave_requests = db.relationship(
        'LeaveRequest',
        backref='employee',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Employee {self.full_name} ({self.department})>"