import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('TRADIE_SECRET_KEY') or 'secret-key-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TRADIE_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')