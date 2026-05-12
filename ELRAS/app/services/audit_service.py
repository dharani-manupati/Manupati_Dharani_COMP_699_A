from app.database import db
from app.models.audit_log import AuditLog


class AuditService:

    @staticmethod
    def log(user_id, action, description=None,
            entity_type=None, entity_id=None,
            role=None, ip_address=None, user_agent=None,
            commit=False):
        """
        Central logging method for all system actions
        """
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            role=role,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.session.add(log_entry)

        if commit:
            db.session.commit()

        return log_entry

    @staticmethod
    def log_user_action(user, action, description=None, commit=False):
        """
        Simplified logging using user object
        """
        return AuditService.log(
            user_id=user.id,
            action=action,
            description=description,
            role=user.role,
            commit=commit
        )

    @staticmethod
    def log_entity_action(user_id, action, entity_type, entity_id,
                         description=None, role=None, commit=False):
        """
        Log action related to a specific entity
        """
        return AuditService.log(
            user_id=user_id,
            action=action,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            role=role,
            commit=commit
        )

    @staticmethod
    def get_logs(limit=100):
        """
        Fetch latest audit logs
        """
        return AuditLog.query.order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_user_logs(user_id):
        """
        Fetch logs for a specific user
        """
        return AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.created_at.desc()).all()

    @staticmethod
    def delete_old_logs():
        """
        Optional: clear old logs (not recommended in production)
        """
        AuditLog.query.delete()
        db.session.commit()
        return True, "All logs deleted"