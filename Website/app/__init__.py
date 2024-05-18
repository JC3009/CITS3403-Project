from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    from app.blueprints import main
    flaskApp.register_blueprint(main)
    db.init_app(flaskApp)
    login.init_app(flaskApp)
    return flaskApp

from app import models