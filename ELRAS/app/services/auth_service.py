from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models.user import User
from app.models.employee import Employee
from app.models.manager import Manager
from app.models.hr_admin import HRAdmin
from app.models.audit_log import AuditLog
from datetime import date


class AuthService:

    @staticmethod
    def register_user(data):
        """
        Register new user (Employee / Manager / HR)
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Check existing user
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return False, "User already exists"

        # Hash password
        password_hash = generate_password_hash(password)

        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        # Create role-specific profile
        if role == 'employee':
            employee = Employee(
                user_id=user.id,
                full_name=data.get('full_name'),
                department=data.get('department'),
                designation=data.get('designation'),
                join_date=data.get('join_date', date.today())
            )
            db.session.add(employee)

        elif role == 'manager':
            manager = Manager(
                user_id=user.id,
                full_name=data.get('full_name'),
                department=data.get('department')
            )
            db.session.add(manager)

        elif role == 'hr':
            hr = HRAdmin(
                user_id=user.id,
                full_name=data.get('full_name'),
                email=email
            )
            db.session.add(hr)

        # Audit log
        AuditLog.log_action(
            user_id=user.id,
            action="User Registered",
            description=f"{role} account created",
            role=role
        )

        db.session.commit()
        return True, "Registration successful"

    @staticmethod
    def login_user(username, password):
        """
        Authenticate user
        """
        user = User.query.filter_by(username=username).first()

        if not user:
            return None, "User not found"

        if not check_password_hash(user.password_hash, password):
            return None, "Invalid password"

        if not user.is_active:
            return None, "Account is inactive"

        # Audit log
        AuditLog.log_action(
            user_id=user.id,
            action="User Login",
            description="User logged into system",
            role=user.role
        )

        return user, "Login successful"

    @staticmethod
    def deactivate_user(user_id):
        """
        Disable user account
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"

        user.is_active = False

        AuditLog.log_action(
            user_id=user.id,
            action="Account Deactivated",
            description="User account disabled",
            role=user.role
        )

        db.session.commit()
        return True, "User deactivated"

    @staticmethod
    def activate_user(user_id):
        """
        Enable user account
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"

        user.is_active = True

        AuditLog.log_action(
            user_id=user.id,
            action="Account Activated",
            description="User account enabled",
            role=user.role
        )

        db.session.commit()
        return True, "User activated"