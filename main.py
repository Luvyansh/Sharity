from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from applications.config import Config
from applications.database import db
from applications.models import User, Role
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        admin_user = User.query.filter_by(email='admin@sharity.com').first()
        if not admin_user:
            admin_user = User(email='admin@sharity.com', password='admin', name='Share Man', dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date())
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
            db.session.commit()
    return app

app = create_app()

from applications.routes import *
from controllers.controllers import *
from applications.sharity import *

from dotenv import load_dotenv
load_dotenv()
import os
app.config["ALPHA_VANTAGE_API_KEY"] = os.getenv("ALPHA_VANTAGE_API_KEY")

if __name__ == "__main__":
    app.run(debug=True)