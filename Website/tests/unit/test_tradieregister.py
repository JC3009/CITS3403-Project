import pytest
from app.controllers import existing_tradie_controller, TradieExistsError
from app.models import User, TradieUser

@pytest.fixture

def user():
    # Create a test user
    return User(username='testuser', email='testuser@example.com')

def test_existing_tradie_controller_no_existing_tradie(user):
    # Create a mock tradie user without an existing tradie account
    user_id = 1
    tradie = None

    assert existing_tradie_controller(user_id, tradie) is None

def test_existing_tradie_controller_existing_tradie(user):
    user_id = 1 
    tradie = TradieUser(user=user, trade='Plumber', hourlyRate=50.0, calloutFee=20.0, certified=True)

    # Call existing_tradie_controller with a user with an existing tradie account
    with pytest.raises(TradieExistsError):
        existing_tradie_controller(user_id, tradie)