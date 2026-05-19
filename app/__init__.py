"""
Numerical Methods Calculator — modular monolith application factory.
"""
import os

from flask import Flask

from app.core.method_registry import registry
from app.extensions import db, login_manager


def create_app(config_name="dev"):
    """Create and configure the Flask application."""
    from app.config import config

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    registry.discover("app.methods")

    from app.routes import main_bp
    from app.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()

    return app
