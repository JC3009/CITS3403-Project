import pytest
from app import create_app, db
from app.models import User, TradieUser, JobRequest, JobOffer

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')  # Assuming 'testing' configuration in your app factory
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def _db(app):
    """Set up the database."""
    db.app = app
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='function')
def session(_db):
    """Create a new database session for each test."""
    with _db.session.begin_nested():
        yield _db.session

@pytest.fixture
def user_data():
    return [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
        # Add more user data as needed
    ]

@pytest.fixture
def tradie_data():
    return [
        {'trade': 'Plumber', 'hourlyRate': 50.0, 'calloutFee': 20.0, 'certified': True},
        {'trade': 'Electrician', 'hourlyRate': 60.0, 'calloutFee': 25.0, 'certified': False},
        # Add more tradie data as needed
    ]

@pytest.fixture
def job_request_data():
    return [
        {'job': 'Fix leaky faucet', 'description': 'The kitchen faucet is leaking.', 'tradeRequired': 'Plumber'},
        {'job': 'Install light fixtures', 'description': 'Install new light fixtures in the living room.', 'tradeRequired': 'Electrician'},
        # Add more job request data as needed
    ]

@pytest.fixture
def populated_db(session, user_data, tradie_data, job_request_data):
    """Populate the database with test data."""
    for user_info in user_data:
        user = User(**user_info)
        user.set_password(user_info['password'])
        session.add(user)

    for tradie_info in tradie_data:
        tradie = TradieUser(**tradie_info)
        session.add(tradie)

    for job_request_info in job_request_data:
        job_request = JobRequest(**job_request_info)
        session.add(job_request)

    session.commit()