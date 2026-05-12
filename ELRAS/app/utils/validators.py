import re
from datetime import datetime


class Validators:

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        # At least 6 chars
        return len(password) >= 6

    @staticmethod
    def validate_required_fields(data, fields):
        for field in fields:
            if not data.get(field):
                return False, f"{field} is required"
        return True, "Valid"

    @staticmethod
    def validate_dates(start_date, end_date):
        try:
            s = datetime.strptime(start_date, "%Y-%m-%d")
            e = datetime.strptime(end_date, "%Y-%m-%d")
            if e < s:
                return False, "End date cannot be before start date"
            return True, "Valid"
        except:
            return False, "Invalid date format"