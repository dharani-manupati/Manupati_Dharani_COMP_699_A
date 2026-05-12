from app.database import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)

    # Who performed the action (User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Action Details
    action = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    # Entity Tracking (what was affected)
    entity_type = db.Column(db.String(50))  # e.g., 'leave_request', 'user', 'policy'
    entity_id = db.Column(db.Integer)

    # Role at the time of action
    role = db.Column(db.String(20))  # employee, manager, hr

    # Metadata (optional but useful)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # BUSINESS LOGIC METHODS
    # =========================

    @staticmethod
    def log_action(user_id, action, description=None,
                   entity_type=None, entity_id=None,
                   role=None, ip_address=None, user_agent=None):
        """
        Create a new audit log entry
        """
        log = AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            role=role,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(log)
        return log

    def __repr__(self):
        return f"<AuditLog User:{self.user_id} Action:{self.action}>"