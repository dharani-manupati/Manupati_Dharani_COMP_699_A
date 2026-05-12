from app.models.leave_request import LeaveRequest
from app.models.employee import Employee
from app.models.leave_balance import LeaveBalance
from app.models.leave_policy import LeavePolicy
from app.models.user import User
from app.database import db
from sqlalchemy import func


class ReportService:

    @staticmethod
    def get_leave_summary():
        """
        Overall leave statistics (HR dashboard)
        """
        total_requests = LeaveRequest.query.count()

        approved = LeaveRequest.query.filter_by(status='approved').count()
        rejected = LeaveRequest.query.filter_by(status='rejected').count()
        pending = LeaveRequest.query.filter_by(status='pending').count()

        return {
            "total_requests": total_requests,
            "approved": approved,
            "rejected": rejected,
            "pending": pending
        }

    @staticmethod
    def get_employee_leave_report(employee_id):
        """
        Detailed leave report for a specific employee
        """
        leaves = LeaveRequest.query.filter_by(user_id=employee_id).all()

        report = []
        for leave in leaves:
            report.append({
                "leave_type": leave.leave_type,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "days": leave.total_days,
                "status": leave.status
            })

        return report

    @staticmethod
    def get_department_report():
        """
        Leave usage grouped by department
        """
        results = db.session.query(
            Employee.department,
            func.count(LeaveRequest.id),
            func.sum(LeaveRequest.total_days)
        ).join(LeaveRequest, Employee.user_id == LeaveRequest.user_id) \
         .group_by(Employee.department).all()

        report = []
        for dept, count, days in results:
            report.append({
                "department": dept,
                "total_requests": count,
                "total_days": days or 0
            })

        return report

    @staticmethod
    def get_leave_balance_report():
        """
        Remaining leave balances for all employees
        """
        balances = LeaveBalance.query.all()

        report = []
        for b in balances:
            report.append({
                "employee_id": b.employee_id,
                "leave_type": b.leave_type,
                "total": b.total_allocated,
                "used": b.used,
                "remaining": b.remaining
            })

        return report

    @staticmethod
    def get_policy_report():
        """
        List all policies
        """
        policies = LeavePolicy.query.all()

        report = []
        for p in policies:
            report.append({
                "policy_name": p.policy_name,
                "leave_type": p.leave_type,
                "max_days_per_year": p.max_days_per_year,
                "max_days_per_request": p.max_days_per_request,
                "is_active": p.is_active
            })

        return report

    @staticmethod
    def get_user_statistics():
        """
        Count users by role
        """
        employees = User.query.filter_by(role='employee').count()
        managers = User.query.filter_by(role='manager').count()
        hr = User.query.filter_by(role='hr').count()

        return {
            "employees": employees,
            "managers": managers,
            "hr_admins": hr
        }