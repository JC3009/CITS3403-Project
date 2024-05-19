import pytest
from app.controllers import login_user_controller, LoginError
from app.models import User

@pytest.fixture

def user():
    # Create a test user
    return User(username='testuser', email='testuser@example.com')

def test_login_user_controller_valid(user):
    # Set the password for the test user
    user.set_password('password123')

    # Call login_user_controller with correct credentials
    assert login_user_controller(user, 'password123') is None

def test_login_user_controller_invalid_password(user):
    # Set an incorrect password for the test user
    user.set_password('password123')

    # Call login_user_controller with incorrect password
    with pytest.raises(LoginError):
        login_user_controller(user, 'wrongpassword')

def test_login_user_controller_invalid_user():
    # Create a mock user without setting a password
    user = User(username='testuser', email='testuser@example.com')

    # Call login_user_controller with a user without a password set
    with pytest.raises(LoginError):
        login_user_controller(user, 'password123')