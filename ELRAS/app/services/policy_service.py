from app.database import db
from app.models.leave_policy import LeavePolicy
from app.models.leave_balance import LeaveBalance
from app.models.employee import Employee
from app.models.audit_log import AuditLog


class PolicyService:

    @staticmethod
    def create_policy(data, hr_user_id):
        """
        HR creates a new leave policy
        """
        policy = LeavePolicy(
            policy_name=data.get('policy_name'),
            leave_type=data.get('leave_type'),
            max_days_per_year=data.get('max_days_per_year'),
            max_days_per_request=data.get('max_days_per_request'),
            carry_forward=data.get('carry_forward', False),
            carry_forward_limit=data.get('carry_forward_limit', 0),
            requires_approval=data.get('requires_approval', True),
            allow_half_day=data.get('allow_half_day', False),
            min_days_notice=data.get('min_days_notice', 0),
            max_consecutive_days=data.get('max_consecutive_days', 0),
            created_by=hr_user_id
        )

        db.session.add(policy)

        # Audit log
        AuditLog.log_action(
            user_id=hr_user_id,
            action="Policy Created",
            description=f"{policy.leave_type} policy created",
            entity_type="policy",
            entity_id=None,
            role="hr"
        )

        db.session.commit()
        return True, "Policy created successfully"

    @staticmethod
    def update_policy(policy_id, data, hr_user_id):
        """
        Update existing policy
        """
        policy = LeavePolicy.query.get(policy_id)
        if not policy:
            return False, "Policy not found"

        # Update fields
        policy.policy_name = data.get('policy_name', policy.policy_name)
        policy.max_days_per_year = data.get('max_days_per_year', policy.max_days_per_year)
        policy.max_days_per_request = data.get('max_days_per_request', policy.max_days_per_request)
        policy.carry_forward = data.get('carry_forward', policy.carry_forward)
        policy.carry_forward_limit = data.get('carry_forward_limit', policy.carry_forward_limit)
        policy.requires_approval = data.get('requires_approval', policy.requires_approval)
        policy.allow_half_day = data.get('allow_half_day', policy.allow_half_day)
        policy.min_days_notice = data.get('min_days_notice', policy.min_days_notice)
        policy.max_consecutive_days = data.get('max_consecutive_days', policy.max_consecutive_days)
        policy.is_active = data.get('is_active', policy.is_active)

        # Audit log
        AuditLog.log_action(
            user_id=hr_user_id,
            action="Policy Updated",
            description=f"Policy ID {policy_id} updated",
            entity_type="policy",
            entity_id=policy_id,
            role="hr"
        )

        db.session.commit()
        return True, "Policy updated successfully"

    @staticmethod
    def deactivate_policy(policy_id, hr_user_id):
        """
        Disable a policy
        """
        policy = LeavePolicy.query.get(policy_id)
        if not policy:
            return False, "Policy not found"

        policy.is_active = False

        AuditLog.log_action(
            user_id=hr_user_id,
            action="Policy Deactivated",
            description=f"Policy ID {policy_id} deactivated",
            entity_type="policy",
            entity_id=policy_id,
            role="hr"
        )

        db.session.commit()
        return True, "Policy deactivated"

    @staticmethod
    def assign_policy_to_all_employees(policy_id, hr_user_id):
        """
        Assign leave balance to all employees based on policy
        """
        policy = LeavePolicy.query.get(policy_id)
        if not policy:
            return False, "Policy not found"

        employees = Employee.query.all()

        for emp in employees:
            existing = LeaveBalance.query.filter_by(
                employee_id=emp.id,
                leave_type=policy.leave_type
            ).first()

            if not existing:
                balance = LeaveBalance(
                    employee_id=emp.id,
                    leave_type=policy.leave_type,
                    total_allocated=policy.max_days_per_year,
                    remaining=policy.max_days_per_year,
                    used=0,
                    updated_by=hr_user_id
                )
                db.session.add(balance)

        AuditLog.log_action(
            user_id=hr_user_id,
            action="Policy Assigned",
            description=f"Policy {policy.leave_type} assigned to all employees",
            entity_type="policy",
            entity_id=policy_id,
            role="hr"
        )

        db.session.commit()
        return True, "Policy assigned to all employees"

    @staticmethod
    def get_active_policies():
        """
        Get all active policies
        """
        return LeavePolicy.query.filter_by(is_active=True).all()