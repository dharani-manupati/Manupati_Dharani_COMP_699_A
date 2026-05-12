from app.database import db
from datetime import datetime


class Manager(db.Model):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True)

    # Link to User (login account)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    # Manager Details
    full_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    # Optional level
    level = db.Column(db.String(50), default='manager')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # RELATIONSHIPS
    # =========================

    # One manager → many employees
    team_members = db.relationship(
        'Employee',
        backref='manager',
        lazy=True
    )

    # 🔥 Correct relationship with LeaveRequest
    leave_requests = db.relationship(
        'LeaveRequest',
        backref='manager',
        lazy=True,
        foreign_keys='LeaveRequest.manager_id'
    )

    def __repr__(self):
        return f"<Manager {self.full_name} - {self.department}>"