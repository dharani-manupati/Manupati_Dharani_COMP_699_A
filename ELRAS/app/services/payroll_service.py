from app.models.employee import Employee
from app.models.leave_request import LeaveRequest
from app.models.leave_balance import LeaveBalance
from app.database import db


class PayrollService:

    @staticmethod
    def calculate_salary(employee_id, base_salary, working_days=30):
        """
        Calculate final salary after leave deductions
        """
        employee = Employee.query.get(employee_id)
        if not employee:
            return False, "Employee not found"

        # Get approved leaves
        leaves = LeaveRequest.query.filter_by(
            user_id=employee.user_id,
            status='approved'
        ).all()

        total_leave_days = sum([leave.total_days for leave in leaves])

        # Calculate per day salary
        per_day_salary = base_salary / working_days

        # Deduction (simple logic: unpaid leaves)
        deduction = total_leave_days * per_day_salary

        final_salary = base_salary - deduction

        return {
            "employee_id": employee_id,
            "base_salary": base_salary,
            "leave_days": total_leave_days,
            "deduction": deduction,
            "final_salary": final_salary
        }

    @staticmethod
    def calculate_leave_deduction(employee_id, leave_type):
        """
        Calculate deduction based on specific leave type
        (example: unpaid leave only)
        """
        employee = Employee.query.get(employee_id)
        if not employee:
            return False, "Employee not found"

        leaves = LeaveRequest.query.filter_by(
            user_id=employee.user_id,
            leave_type=leave_type,
            status='approved'
        ).all()

        total_days = sum([leave.total_days for leave in leaves])

        return {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "total_days": total_days
        }

    @staticmethod
    def get_employee_payroll_summary(employee_id):
        """
        Summary of employee leave impact (for reports)
        """
        employee = Employee.query.get(employee_id)
        if not employee:
            return False, "Employee not found"

        balances = LeaveBalance.query.filter_by(employee_id=employee_id).all()

        summary = []
        for b in balances:
            summary.append({
                "leave_type": b.leave_type,
                "total": b.total_allocated,
                "used": b.used,
                "remaining": b.remaining
            })

        return {
            "employee_id": employee_id,
            "leave_summary": summary
        }

    @staticmethod
    def monthly_leave_report(employee_id, month, year):
        """
        Get leave taken in a specific month
        """
        employee = Employee.query.get(employee_id)
        if not employee:
            return False, "Employee not found"

        leaves = LeaveRequest.query.filter(
            LeaveRequest.user_id == employee.user_id,
            LeaveRequest.status == 'approved',
            db.extract('month', LeaveRequest.start_date) == month,
            db.extract('year', LeaveRequest.start_date) == year
        ).all()

        total_days = sum([leave.total_days for leave in leaves])

        return {
            "employee_id": employee_id,
            "month": month,
            "year": year,
            "leave_days": total_days
        }