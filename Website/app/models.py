from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    tradie: so.Mapped['TradieUser'] = so.relationship('TradieUser', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"name: {self.username} contact: {self.email}" #str conversion

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

#to be updated for db integration
class TradieUser(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    trade: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    hourlyRate: so.Mapped[float] = so.mapped_column(sa.Float)
    calloutFee: so.Mapped[float] = so.mapped_column(sa.Float)
    certified: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=0)#functionality which allows the user to be considered certified through external process if they provide their valid trade license
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True) #The user account associated with this tradie account

    user: so.Mapped[User] = so.relationship('User', back_populates='tradie')

    def __repr__(self):
        return f"user: {self.user_id} does {self.trade}" #str conversion

#to be updated for db integration
class Location:
    def __init__(self, streetNumber:str, street:str, suburb:str, postcode:str, state:str) -> None:
        self.streetNumber:str = streetNumber
        self.street:str = street
        self.suburb:str = suburb
        self.postcode:str = postcode
        self.state:str = state

    def __repr__(self):
        return f"{self.streetNumber} {self.street}, {self.suburb}, {self.state}, {self.postcode}" #str conversion
    
#to be updated for db integration
class JobRequest:
    def __init__(self, requestor:User, job:str, description:str, location:Location, dateCreated:str, timeCreated:str) -> None:
        self.userName:str = requestor.username
        self.userEmail:str = requestor.email
        self.job:str = job
        self.description:str = description
        self.location:Location = location
        self.dateCreated:str = dateCreated #date format: dd/mm/yyyy
        self.timeCreated:str = timeCreated #time format: hh:mm

    def __repr__(self):
        return f"{self.userName} requested {self.job} at {self.location} on {self.dateCreated} at {self.timeCreated}"

#to be updated for db integration
class JobOffer:
    def __init__(self, tradie:TradieUser, jobRequest:JobRequest, dateOffered:str, timeOffered:str, timeEstimate:float) -> None:
        self.tradieName:str = tradie.username
        self.tradieEmail:str = tradie.email
        self.jobRequest:JobRequest = jobRequest
        self.timeEstimate:float = timeEstimate
        self.costEstimate:float = tradie.calloutFee + tradie.hourlyRate * timeEstimate
        self.dateOffered:str = dateOffered #date format: dd/mm/yyyy
        self.timeOffered:str = timeOffered #time format: hh:mm

    def __repr__(self):
        return f"Tradie: {self.tradieName} offered to complete {self.jobRequest.job} for {self.costEstimate} on {self.dateOffered} at {self.timeOffered}"