from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, date, timezone
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    tradie: so.Mapped['TradieUser'] = so.relationship('TradieUser', back_populates='user')
    jobRequests: so.Mapped['JobRequest'] = so.relationship('JobRequest', back_populates='creator')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"name: {self.username} contact: {self.email}" # str conversion

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    data: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary)

class TradieUser(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    trade: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    hourlyRate: so.Mapped[float] = so.mapped_column(sa.Float)
    calloutFee: so.Mapped[float] = so.mapped_column(sa.Float)
    certified: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)  # Use False for default value
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True) # The user account associated with this tradie account

    user: so.Mapped[User] = so.relationship('User', back_populates='tradie')
    jobOffers: so.Mapped['JobOffer'] = so.relationship('JobOffer', back_populates='tradie')

    def __repr__(self):
        return f"user: {self.user_id} does {self.trade}" # str conversion

class Location(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    streetNumber: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    street: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    suburb: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    postcode: so.Mapped[str] = so.mapped_column(sa.String(8), index=True)
    state: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)

    jobRequests: so.Mapped['JobRequest'] = so.relationship('JobRequest', back_populates='Location')

    def __repr__(self):
        return f"{self.streetNumber} {self.street}, {self.suburb}, {self.state}, {self.postcode}" # str conversion

class JobRequest(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    job: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    datetimeCreated: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    location_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('location.id'), index=True) # The location the job is to be completed at
    location: so.Mapped[Location] = so.relationship('location', back_populates='jobRequests')

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True) # The user account associated with this job request
    creator: so.Mapped[User] = so.relationship('User', back_populates='jobRequests')

    jobOffers: so.Mapped['JobOffer'] = so.relationship('JobOffer', back_populates='jobRequest')

    def __repr__(self):
        return f"{self.creator.username} requested {self.job} at {self.location} on {self.datetimeCreated}"

class JobOffer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    timeEstimate: so.Mapped[float] = so.mapped_column(sa.Float) # time in hours
    dateOffered: so.Mapped[date] = so.mapped_column(sa.Date, index=True)

    jobRequest_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('job_request.id'), index=True)
    jobRequest: so.Mapped[JobRequest] = so.relationship('JobRequest', back_populates='jobOffers')

    tradie_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('tradie_user.id'), index=True)
    tradie: so.Mapped[TradieUser] = so.relationship('TradieUser', back_populates='jobOffers')

    def __repr__(self):
        return f"Tradie: {self.tradie.user.username} offered to complete {self.jobRequest.job} on {self.dateOffered} for an estimated {self.timeEstimate} hours"
   