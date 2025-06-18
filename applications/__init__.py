import os
from flask import Flask
from .config import Config
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import and register blueprints or routes
        from . import routes
        app.register_blueprint(routes.bp)  # if you use Blueprint

        # Initialize DB tables if needed
        db.create_all()

    return app
