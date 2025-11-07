from flask import Flask
from sqlalchemy import select

from .extensions import db, login_manager
from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .models import User
from .errors import register_errors
from .commands import register_commands
from .settings import config


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    db.init_app(app)
    login_manager.init_app(app)

    register_errors(app)
    register_commands(app)

    @app.context_processor
    def inject_user():
        user = db.session.scalar(select(User))
        return dict(user=user)

    return app
