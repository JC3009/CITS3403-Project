import sqlalchemy as sa
import sqlalchemy.orm as so
from app import flaskApp, db
from app.models import User, TradieUser

@flaskApp.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'TradieUser': TradieUser}
