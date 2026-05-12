from app.database import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)

    # Who receives the notification (User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Message content
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Type of notification (for UI handling)
    type = db.Column(db.String(50), default='info')
    # values: info, success, warning, error

    # Related entity (optional, for linking actions)
    related_id = db.Column(db.Integer)  # e.g., leave_request_id
    related_type = db.Column(db.String(50))  # e.g., 'leave_request'

    # Status
    is_read = db.Column(db.Boolean, default=False)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # BUSINESS LOGIC METHODS
    # =========================

    def mark_as_read(self):
        """
        Mark notification as read
        """
        self.is_read = True

    def mark_as_unread(self):
        """
        Mark notification as unread
        """
        self.is_read = False

    def __repr__(self):
        return f"<Notification User:{self.user_id} Type:{self.type}>"