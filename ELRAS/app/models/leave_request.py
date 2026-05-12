from app.database import db
from datetime import datetime


class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    # =========================
    # PRIMARY KEY
    # =========================
    id = db.Column(db.Integer, primary_key=True)

    # =========================
    # FOREIGN KEYS
    # =========================

    # Employee who applied leave
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )

    # 🔥 REQUIRED: Manager who will approve/reject
    manager_id = db.Column(
        db.Integer,
        db.ForeignKey('managers.id'),
        nullable=True
    )

    # =========================
    # LEAVE DETAILS
    # =========================
    leave_type = db.Column(db.String(50), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    total_days = db.Column(db.Integer)

    reason = db.Column(db.Text)

    # =========================
    # APPROVAL DETAILS
    # =========================
    status = db.Column(
        db.String(20),
        default='pending'   # pending / approved / rejected
    )

    manager_comments = db.Column(db.Text)

    # =========================
    # TIMESTAMP
    # =========================
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =========================
    # HELPER METHOD
    # =========================
    def calculate_total_days(self):
        """Calculate total leave days"""
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1

    def __repr__(self):
        return f"<LeaveRequest {self.id} | {self.status}>"