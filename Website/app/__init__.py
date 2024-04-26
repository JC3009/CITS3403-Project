from flask import Flask
from config import Config

flaskApp = Flask(__name__)
flaskapp.config.from_object(Config)

from app import routes