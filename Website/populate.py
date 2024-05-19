from webServer import db, flaskApp
from app.models import User, TradieUser, JobRequest, JobOffer
from datetime import datetime, date, timezone
import random

with flaskApp.app_context():

    # Create users
    users_data = [
        {'username': 'tradie1', 'email': 'tradie1@example.com', 'password': 'password1'},
        {'username': 'tradie2', 'email': 'tradie2@example.com', 'password': 'password2'},
        {'username': 'tradie3', 'email': 'tradie3@example.com', 'password': 'password3'},
        {'username': 'user4', 'email': 'user4@example.com', 'password': 'password4'},
        {'username': 'user5', 'email': 'user5@example.com', 'password': 'password5'},
        {'username': 'user6', 'email': 'user6@example.com', 'password': 'password6'},
    ]

    for user_data in users_data:
        user = User(username=user_data['username'], email=user_data['email'])
        user.set_password(user_data['password'])
        db.session.add(user)
    db.session.commit()

    # Create tradies
    tradies_data = [
        {'trade': 'Plumber', 'hourlyRate': 50.0, 'calloutFee': 20.0, 'certified': True, 'user_id': 1},
        {'trade': 'Electrician', 'hourlyRate': 60.0, 'calloutFee': 30.0, 'certified': True, 'user_id': 2},
        {'trade': 'Carpenter', 'hourlyRate': 55.0, 'calloutFee': 25.0, 'certified': False, 'user_id': 3},
    ]

    for tradie_data in tradies_data:
        tradie = TradieUser(**tradie_data)
        db.session.add(tradie)
    db.session.commit()

    # Create job requests for non-tradie users
    job_requests_data = [
        {'job': 'Fix leaking pipe', 'description': 'Pipe leaking in the kitchen', 'streetNumber': '123', 'street': 'Main St', 'suburb': 'Suburbia', 'postcode': '1235', 'state': 'WA', 'tradeRequired': 'Plumber', 'user_id': 4},
        {'job': 'Install new light', 'description': 'Need a new light installed in the living room', 'streetNumber': '456', 'street': 'Elm St', 'suburb': 'Suburbia', 'postcode': '12345', 'state': 'NSW', 'tradeRequired': 'Electrician', 'user_id': 4},
        {'job': 'Build a new deck', 'description': 'Want a new deck built in the backyard', 'streetNumber': '789', 'street': 'Pine St', 'suburb': 'Suburbia', 'postcode': '145', 'state': 'NT', 'tradeRequired': 'Carpenter', 'user_id': 4},
        
        {'job': 'Unclog drain', 'description': 'Drain in the bathroom is clogged', 'streetNumber': '123', 'street': 'Main St', 'suburb': 'Suburbia', 'postcode': '54', 'state': 'SA', 'tradeRequired': 'Plumber', 'user_id': 5},
        {'job': 'Replace socket', 'description': 'Need a new socket installed', 'streetNumber': '456', 'street': 'Elm St', 'suburb': 'Suburbia', 'postcode': '23', 'state': 'WA', 'tradeRequired': 'Electrician', 'user_id': 5},
        {'job': 'Fix door frame', 'description': 'Door frame needs repair', 'streetNumber': '789', 'street': 'Pine St', 'suburb': 'Suburbia', 'postcode': '12', 'state': 'State', 'tradeRequired': 'Carpenter', 'user_id': 5},
        
        {'job': 'Install dishwasher', 'description': 'Need a dishwasher installed', 'streetNumber': '123', 'street': 'Main St', 'suburb': 'Suburbia', 'postcode': '123', 'state': 'State', 'tradeRequired': 'Plumber', 'user_id': 6},
        {'job': 'Fix circuit breaker', 'description': 'Circuit breaker keeps tripping', 'streetNumber': '456', 'street': 'Elm St', 'suburb': 'Suburbia', 'postcode': '1245', 'state': 'State', 'tradeRequired': 'Electrician', 'user_id': 6},
        {'job': 'Install shelves', 'description': 'Need shelves installed in the garage', 'streetNumber': '789', 'street': 'Pine St', 'suburb': 'Suburbia', 'postcode': '145', 'state': 'State', 'tradeRequired': 'Carpenter', 'user_id': 6},
    ]

    for job_request_data in job_requests_data:
        job_request = JobRequest(**job_request_data, datetimeCreated=datetime.now(timezone.utc))
        db.session.add(job_request)
    db.session.commit()

    # Create job offers from tradies
    job_offers_data = []

    job_requests = JobRequest.query.all()
    tradies = TradieUser.query.all()

    for job_request in job_requests:
        for tradie in tradies:
            if job_request.tradeRequired == tradie.trade:
                job_offer = JobOffer(
                    timeEstimate=random.uniform(1.0, 5.0),
                    dateOffered=date.today(),
                    acceptedStatus=False,
                    jobRequest_id=job_request.id,
                    tradie_id=tradie.id
                )
                job_offers_data.append(job_offer)

    for job_offer in job_offers_data:
        db.session.add(job_offer)
    db.session.commit()

    print("Database populated with test data.")