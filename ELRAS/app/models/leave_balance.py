from app.database import db
from datetime import datetime


class LeaveBalance(db.Model):
    __tablename__ = 'leave_balances'

    id = db.Column(db.Integer, primary_key=True)

    # Link to Employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    # Leave Type (Sick, Casual, Annual)
    leave_type = db.Column(db.String(50), nullable=False)

    # Balance Tracking
    total_allocated = db.Column(db.Integer, default=0)
    used = db.Column(db.Integer, default=0)
    remaining = db.Column(db.Integer, default=0)

    # HR who last updated this balance
    updated_by = db.Column(db.Integer, db.ForeignKey('hr_admins.id'), nullable=True)

    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Ensure one record per employee per leave type
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'leave_type', name='unique_employee_leave_type'),
    )

    # =========================
    # BUSINESS LOGIC METHODS
    # =========================

    def allocate_leaves(self, days):
        """
        HR allocates leaves
        """
        self.total_allocated += days
        self.remaining += days

    def deduct_leaves(self, days):
        """
        Deduct leave when approved
        """
        if self.remaining >= days:
            self.used += days
            self.remaining -= days
            return True
        return False

    def add_back_leaves(self, days):
        """
        Add back leaves (if cancelled/rejected after approval)
        """
        self.used -= days
        self.remaining += days

    def adjust_balance(self, new_total):
        """
        HR manually adjusts total balance
        """
        difference = new_total - self.total_allocated
        self.total_allocated = new_total
        self.remaining += difference

    def __repr__(self):
        return f"<LeaveBalance Emp:{self.employee_id} Type:{self.leave_type} Remaining:{self.remaining}>"