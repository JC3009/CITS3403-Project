import pytest
from app.controllers import job_request_controller, JobRequestError
from app.models import User, JobRequest

@pytest.fixture

def user():
    # Create a test user
    return User(username='testuser', email='testuser@example.com')

def test_job_request_controller_valid(user):
    # Create a mock job request author
    job_request_author_id = 1 

    assert job_request_controller(job_request_author_id, 1, False, False) is None

def test_job_request_controller_unauthorized(user):
    # Create a mock job request author
    job_request_author_id = 1 

    # Call job_request_controller with unauthorized user
    with pytest.raises(JobRequestError):
        job_request_controller(job_request_author_id, 2, False, False)  # Assuming user ID 2 is not the job request author

def test_job_request_controller_already_accepted(user):
    job_request_author_id = 1

    # Call job_request_controller with already accepted offer
    with pytest.raises(JobRequestError):
        job_request_controller(job_request_author_id, 1, True, False)

def test_job_request_controller_already_rejected(user):
    job_request_author_id = 1 

    # Call job_request_controller with already rejected offer
    with pytest.raises(JobRequestError):
        job_request_controller(job_request_author_id, 1, False, True)