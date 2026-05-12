from flask import Flask
from config import Config

from app.database import db, init_extensions
from app.routes import register_routes

# Import all models (VERY IMPORTANT for db.create_all)
from app.models.user import User
from app.models.employee import Employee
from app.models.manager import Manager
from app.models.hr_admin import HRAdmin
from app.models.leave_request import LeaveRequest
from app.models.leave_balance import LeaveBalance
from app.models.leave_policy import LeavePolicy
from app.models.notification import Notification
from app.models.document import Document
from app.models.audit_log import AuditLog


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Initialize extensions (DB, Login)
    init_extensions(app)

    # Register routes
    register_routes(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app