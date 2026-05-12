from app.routes.auth_routes import auth_bp
from app.routes.employee_routes import employee_bp
from app.routes.manager_routes import manager_bp
from app.routes.hr_routes import hr_bp
from app.routes.common_routes import common_bp


def register_routes(app):

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(employee_bp, url_prefix='/employee')
    app.register_blueprint(manager_bp, url_prefix='/manager')
    app.register_blueprint(hr_bp, url_prefix='/hr')
    app.register_blueprint(common_bp, url_prefix='/')