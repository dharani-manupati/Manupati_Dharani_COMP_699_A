from app.database import db
from datetime import datetime


class LeavePolicy(db.Model):
    __tablename__ = 'leave_policies'

    id = db.Column(db.Integer, primary_key=True)

    # Policy Info
    policy_name = db.Column(db.String(100), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # Sick, Casual, Annual

    # Rules
    max_days_per_year = db.Column(db.Integer, nullable=False)
    max_days_per_request = db.Column(db.Integer, nullable=False)

    carry_forward = db.Column(db.Boolean, default=False)
    carry_forward_limit = db.Column(db.Integer, default=0)

    requires_approval = db.Column(db.Boolean, default=True)
    allow_half_day = db.Column(db.Boolean, default=False)

    # Advanced Rules
    min_days_notice = db.Column(db.Integer, default=0)  # notice before applying
    max_consecutive_days = db.Column(db.Integer, default=0)

    # Status
    is_active = db.Column(db.Boolean, default=True)

    # Created by HR
    created_by = db.Column(db.Integer, db.ForeignKey('hr_admins.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # BUSINESS LOGIC METHODS
    # =========================

    def validate_request(self, total_days):
        """
        Validate leave request against policy rules
        """
        if total_days > self.max_days_per_request:
            return False, f"Exceeds maximum allowed days per request ({self.max_days_per_request})"
        return True, "Valid request"

    def can_carry_forward(self, unused_days):
        """
        Check carry forward eligibility
        """
        if self.carry_forward:
            return min(unused_days, self.carry_forward_limit)
        return 0

    def __repr__(self):
        return f"<LeavePolicy {self.policy_name} ({self.leave_type})>"