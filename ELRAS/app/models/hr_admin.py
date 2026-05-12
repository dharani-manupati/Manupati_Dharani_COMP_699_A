from app.database import db
from datetime import datetime


class HRAdmin(db.Model):
    __tablename__ = 'hr_admins'

    id = db.Column(db.Integer, primary_key=True)

    # Link to User (login account)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    # HR Details
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))

    # Role Info
    role_title = db.Column(db.String(100), default='HR Admin')

    # Permissions
    can_manage_users = db.Column(db.Boolean, default=True)
    can_manage_policies = db.Column(db.Boolean, default=True)
    can_view_reports = db.Column(db.Boolean, default=True)
    can_override_approvals = db.Column(db.Boolean, default=True)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # RELATIONSHIPS (SAFE)
    # =========================

    # HR creates policies (LeavePolicy.created_by → HRAdmin.id)
    policies = db.relationship(
        'LeavePolicy',
        backref='created_by_hr',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # HR updates leave balances (LeaveBalance.updated_by → HRAdmin.id)
    leave_balances = db.relationship(
        'LeaveBalance',
        backref='updated_by_hr',
        lazy=True,
        cascade="all"
    )

    def __repr__(self):
        return f"<HRAdmin {self.full_name}>"