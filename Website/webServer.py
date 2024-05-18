import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_migrate import Migrate
from app import create_app, db
from app.config import DeploymentConfig
from app.models import User, TradieUser

flaskApp = create_app(DeploymentConfig)
migrate = Migrate(flaskApp, db)

@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'TradieUser': TradieUser}
