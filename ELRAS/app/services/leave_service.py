from app.database import db
from app.models.leave_request import LeaveRequest
from app.models.leave_balance import LeaveBalance
from app.models.leave_policy import LeavePolicy
from app.models.document import Document
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.models.employee import Employee
from app.services.notification_service import NotificationService
from datetime import datetime


class LeaveService:

    @staticmethod
    def apply_leave(user_id, data, file=None):
        """
        Apply for leave with validation and optional document
        """

        leave_type = data.get('leave_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reason = data.get('reason')

        # Convert dates
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Validate dates
        if end_date < start_date:
            return False, "End date cannot be before start date"

        # Calculate days
        total_days = (end_date - start_date).days + 1

        # Get employee
        employee = Employee.query.filter_by(user_id=user_id).first()
        if not employee:
            return False, "Employee not found"

        # Get policy
        policy = LeavePolicy.query.filter_by(
            leave_type=leave_type,
            is_active=True
        ).first()

        if not policy:
            return False, "No policy defined for this leave type"

        valid, message = policy.validate_request(total_days)
        if not valid:
            return False, message

        # Check leave balance
        balance = LeaveBalance.query.filter_by(
            employee_id=employee.id,
            leave_type=leave_type
        ).first()

        if not balance or balance.remaining < total_days:
            return False, "Insufficient leave balance"

        # ✅ FIXED: Create leave request correctly
        leave = LeaveRequest(
            employee_id=employee.id,           # ✅ CORRECT
            manager_id=employee.manager_id,    # ✅ IMPORTANT
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            reason=reason,
            status='pending'
        )

        db.session.add(leave)
        db.session.flush()  # get leave.id

        # Handle document upload
        if file:
            document = Document(
                employee_id=employee.id,
                leave_request_id=leave.id,
                file_name=file.filename,
                file_path=f"app/static/uploads/{file.filename}",
                file_type=file.content_type
            )
            db.session.add(document)

        # Notification
        NotificationService.create_notification(
            user_id=user_id,
            title="Leave Applied",
            message=f"Your leave request for {total_days} days is submitted",
            type="info",
            related_id=leave.id,
            related_type="leave_request"
        )

        # Audit log
        AuditLog.log_action(
            user_id=user_id,
            action="Leave Applied",
            description=f"{leave_type} leave for {total_days} days",
            entity_type="leave_request",
            entity_id=leave.id,
            role="employee"
        )

        db.session.commit()
        return True, "Leave applied successfully"

    # =========================
    # CANCEL LEAVE
    # =========================
    @staticmethod
    def cancel_leave(user_id, leave_id):

        leave = LeaveRequest.query.get(leave_id)

        # ✅ FIXED: check via employee
        employee = Employee.query.filter_by(user_id=user_id).first()

        if not leave or not employee or leave.employee_id != employee.id:
            return False, "Leave not found"

        if leave.status != 'pending':
            return False, "Only pending leaves can be cancelled"

        leave.status = 'cancelled'

        # Audit log
        AuditLog.log_action(
            user_id=user_id,
            action="Leave Cancelled",
            description=f"Leave ID {leave_id} cancelled",
            entity_type="leave_request",
            entity_id=leave_id,
            role="employee"
        )

        db.session.commit()
        return True, "Leave cancelled successfully"

    # =========================
    # GET USER LEAVES
    # =========================
    @staticmethod
    def get_user_leaves(user_id):

        employee = Employee.query.filter_by(user_id=user_id).first()

        if not employee:
            return []

        return LeaveRequest.query.filter_by(
            employee_id=employee.id   
        ).order_by(
            LeaveRequest.created_at.desc()   
        ).all()