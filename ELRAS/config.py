import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration for the ELRAS system
    """

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey123"

    # Database (SQLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'elras.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Session Configuration
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Additional Security Headers (basic level)
    REMEMBER_COOKIE_DURATION = 86400  # 1 day