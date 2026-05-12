from app.database import db
from app.models.notification import Notification
from app.models.audit_log import AuditLog


class NotificationService:

    @staticmethod
    def create_notification(user_id, title, message,
                            type="info",
                            related_id=None,
                            related_type=None):
        """
        Create a new notification for a user
        """
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            related_id=related_id,
            related_type=related_type
        )

        db.session.add(notification)

        # Optional: log notification creation
        AuditLog.log_action(
            user_id=user_id,
            action="Notification Created",
            description=title,
            entity_type="notification",
            entity_id=None,
            role=None
        )

        return notification

    @staticmethod
    def get_user_notifications(user_id, only_unread=False):
        """
        Fetch notifications for a user
        """
        query = Notification.query.filter_by(user_id=user_id)

        if only_unread:
            query = query.filter_by(is_read=False)

        return query.order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_as_read(notification_id):
        """
        Mark a single notification as read
        """
        notification = Notification.query.get(notification_id)

        if not notification:
            return False, "Notification not found"

        notification.mark_as_read()
        db.session.commit()

        return True, "Notification marked as read"

    @staticmethod
    def mark_all_as_read(user_id):
        """
        Mark all notifications as read for a user
        """
        notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).all()

        for notif in notifications:
            notif.mark_as_read()

        db.session.commit()
        return True, "All notifications marked as read"

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete a notification
        """
        notification = Notification.query.get(notification_id)

        if not notification:
            return False, "Notification not found"

        db.session.delete(notification)
        db.session.commit()

        return True, "Notification deleted"