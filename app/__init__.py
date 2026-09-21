from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """Application factory for initializing Flask app, extensions, routes, and exception handlers."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy database extension
    db.init_app(app)

    # Register centralized exception handlers
    from app.utils.exception_handler import register_exception_handlers
    register_exception_handlers(app)

    # Register application blueprints
    from app.routes.employee_routes import employee_bp
    app.register_blueprint(employee_bp)

    return app
