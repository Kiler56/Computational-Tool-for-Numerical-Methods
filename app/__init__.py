"""
Calculadora de Métodos Numéricos — Monolito Modular
Application Factory Pattern
"""
import os

from flask import Flask

from app.core.method_registry import registry
from app.extensions import db, login_manager


def create_app(config_name="dev"):
    """Application factory: crea y configura la instancia Flask."""
    from app.config import config

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Callback para cargar usuario por id
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Autodiscovery de métodos numéricos
    registry.discover("app.methods")

    # Registrar blueprints
    from app.routes import main_bp
    from app.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Crear tablas si no existen
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()

    return app
