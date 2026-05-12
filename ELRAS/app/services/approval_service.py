from app.database import db
from app.models.leave_request import LeaveRequest
from app.models.leave_balance import LeaveBalance
from app.models.employee import Employee
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.services.notification_service import NotificationService
from datetime import datetime


class ApprovalService:

    @staticmethod
    def approve_leave(manager_user_id, leave_id, comments=None):
        """
        Manager approves a leave request
        """
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            return False, "Leave request not found"

        if leave.status != 'pending':
            return False, "Only pending requests can be approved"

        # Get manager profile
        manager = Employee.query.filter_by(user_id=manager_user_id).first()
        # NOTE: manager_user_id belongs to User → Manager, but Employee.manager_id links to Manager.id
        # We will validate using manager_id directly from leave

        # Get employee
        employee = Employee.query.filter_by(user_id=leave.user_id).first()
        if not employee:
            return False, "Employee not found"

        # Validate manager ownership
        if employee.manager_id != leave.manager_id:
            return False, "Unauthorized approval action"

        # Get leave balance
        balance = LeaveBalance.query.filter_by(
            employee_id=employee.id,
            leave_type=leave.leave_type
        ).first()

        if not balance:
            return False, "Leave balance not found"

        # Deduct balance
        if not balance.deduct_leaves(leave.total_days):
            return False, "Insufficient leave balance"

        # Approve leave
        leave.approve(leave.manager_id, comments)

        # Notification to employee
        NotificationService.create_notification(
            user_id=leave.user_id,
            title="Leave Approved",
            message=f"Your leave request has been approved",
            type="success",
            related_id=leave.id,
            related_type="leave_request"
        )

        # Audit log
        AuditLog.log_action(
            user_id=manager_user_id,
            action="Leave Approved",
            description=f"Approved leave ID {leave.id}",
            entity_type="leave_request",
            entity_id=leave.id,
            role="manager"
        )

        db.session.commit()
        return True, "Leave approved successfully"

    @staticmethod
    def reject_leave(manager_user_id, leave_id, comments=None):
        """
        Manager rejects a leave request
        """
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            return False, "Leave request not found"

        if leave.status != 'pending':
            return False, "Only pending requests can be rejected"

        # Reject leave
        leave.reject(leave.manager_id, comments)

        # Notification
        NotificationService.create_notification(
            user_id=leave.user_id,
            title="Leave Rejected",
            message=f"Your leave request has been rejected",
            type="error",
            related_id=leave.id,
            related_type="leave_request"
        )

        # Audit log
        AuditLog.log_action(
            user_id=manager_user_id,
            action="Leave Rejected",
            description=f"Rejected leave ID {leave.id}",
            entity_type="leave_request",
            entity_id=leave.id,
            role="manager"
        )

        db.session.commit()
        return True, "Leave rejected successfully"

    @staticmethod
    def hr_override(hr_user_id, leave_id, comments=None):
        """
        HR overrides leave decision
        """
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            return False, "Leave request not found"

        employee = Employee.query.filter_by(user_id=leave.user_id).first()
        if not employee:
            return False, "Employee not found"

        # Get leave balance
        balance = LeaveBalance.query.filter_by(
            employee_id=employee.id,
            leave_type=leave.leave_type
        ).first()

        if not balance:
            return False, "Leave balance not found"

        # If previously rejected → deduct now
        if leave.status == 'rejected':
            if not balance.deduct_leaves(leave.total_days):
                return False, "Insufficient leave balance"

        # Override
        leave.override_by_hr(comments)

        # Notification
        NotificationService.create_notification(
            user_id=leave.user_id,
            title="Leave Overridden by HR",
            message="Your leave has been approved by HR override",
            type="warning",
            related_id=leave.id,
            related_type="leave_request"
        )

        # Audit log
        AuditLog.log_action(
            user_id=hr_user_id,
            action="HR Override",
            description=f"HR approved leave ID {leave.id}",
            entity_type="leave_request",
            entity_id=leave.id,
            role="hr"
        )

        db.session.commit()
        return True, "Leave overridden by HR"