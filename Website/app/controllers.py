from app.models import User, TradieUser
from app import db  


class LoginError(Exception):
    pass

class TradieExistsError(Exception):
    pass

class TradieNotExistsError(Exception):
    pass

class TradeError(Exception):
    pass

class JobRequestError(Exception):
    pass

def login_user_controller(user, password):
    if user is None or not user.check_password(password):
                raise LoginError("Invalid username or password.")
    
def existing_tradie_controller(user_id):
    existing_tradie = db.session.query(TradieUser).filter_by(user_id=user_id).first()
    if existing_tradie:
        raise TradieExistsError("You have already registered as a tradie!")
    if not existing_tradie:
        raise TradieNotExistsError("Only Registered Tradies can access this page!")

def compare_trade_controller(tradie_trade, requiredTrade):
    if tradie_trade != requiredTrade:
        raise TradeError(f"Your trade: {tradie.trade} does not match the required trade: {requiredTrade}!")
    
def job_request_controller(job_request_author, current_user_id, job_offer_accepted, job_offer_rejected):
    if job_request_author != current_user_id:
        raise JobRequestError("You are not the creator of this request!")
    if job_offer_accepted == True:
        raise JobRequestError("You have already accepted this offer!")
    if job_offer_rejected == True:
        raise JobRequestError("You have already rejected this offer!")
    
