import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('TRADIE_SECRET_KEY')

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory'
    TESTING = True