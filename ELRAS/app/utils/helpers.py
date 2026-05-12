from datetime import datetime


class Helpers:

    @staticmethod
    def format_date(date_obj):
        if not date_obj:
            return ""
        return date_obj.strftime("%d-%m-%Y")

    @staticmethod
    def calculate_days(start_date, end_date):
        return (end_date - start_date).days + 1

    @staticmethod
    def get_current_time():
        return datetime.utcnow()

    @staticmethod
    def to_int(value, default=0):
        try:
            return int(value)
        except:
            return default