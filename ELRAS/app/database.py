from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Database instance
db = SQLAlchemy()

# Login manager instance
login_manager = LoginManager()

def init_extensions(app):
    """
    Initialize all extensions with the Flask app
    """
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for session management
    """
    from app.models.user import User
    return User.query.get(int(user_id))