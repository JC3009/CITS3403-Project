from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length, Regexp
import sqlalchemy as sa
from app import db
from app.models import User

#user login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

#New user registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min = 8, message = "Please create a password at least 8 characters long"),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).+$', message = "Please create a password that includes a capital letter, number and special character")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #validate_username and validate_email are custom validators, they will be checked by WTForms when the form is submitted

    #Ensure that username is not already being used
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Username already taken.')

    #Ensure that email is not already being used
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
              raise ValidationError('Email adress already in use.')
        
class JobRequestForm(FlaskForm):
    trades = [('plumber', 'Plumber'), ('electrician', 'Electrician'), ('carpenter', 'Carpenter')]
    streetNumber = StringField('Street Number', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    suburb = StringField('Suburb', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    state = SelectField('State', choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('SA', 'SA'), ('WA', 'WA'), ('TAS', 'TAS'), ('NT', 'NT'), ('ACT', 'ACT')], validators=[DataRequired()])
    tradeRequired = SelectField('Trade Required', choices=trades, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Job Request')

    def validate_postcode(self, postcode):
        if len(postcode.data) != 4 or not postcode.data.isdigit():
            raise ValidationError('Invalid postcode. Postcode must be a 4 digit number.')

    def validate_tradeRequired(self, tradeRequired):
        if tradeRequired.data not in ['plumber', 'electrician', 'carpenter']:
            raise ValidationError('Invalid trade. Please choose from plumber, electrician, carpenter.')

class TradieUserForm(FlaskForm):
    trades = [('plumber', 'Plumber'), ('electrician', 'Electrician'), ('carpenter', 'Carpenter')]
    trade = SelectField('Trade', choices=trades, validators=[DataRequired()])
    hourlyRate = StringField('Hourly Rate', validators=[DataRequired()])
    calloutFee = StringField('Callout Fee', validators=[DataRequired()])
    submit = SubmitField('Register as Tradie')

class JobOfferForm(FlaskForm):
    timeEstimate = FloatField('Time Estimate (hours)', validators=[DataRequired(), NumberRange(min=0, message="Time estimate must be a positive number")])
    dateOffered = DateField('Date Offered', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit Job Offer')

class RespondToOfferForm(FlaskForm):
    response = SelectField('Response', choices=[('accept', 'Accept'), ('reject', 'Reject')], validators=[DataRequired()])
    submit = SubmitField('Respond to Offer')

class RequestSearchForm(FlaskForm):
    tradeFilter = SelectField('Trade', choices=[('all', 'All'), ('plumber', 'Plumber'), ('electrician', 'Electrician'), ('carpenter', 'Carpenter')], validators=[DataRequired()])
    stateFilter = SelectField('State', choices=[('all', 'All'), ('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('SA', 'SA'), ('WA', 'WA'), ('TAS', 'TAS'), ('NT', 'NT'), ('ACT', 'ACT')], validators=[DataRequired()])
    postcodeFilter = StringField('Postcode')
    order = SelectField('Order by', choices=[('datetimeCreated', 'Date Created'), ('job', 'Job'), ('state', 'State'), ('postcode', 'Postcode')], validators=[DataRequired()])
    submit = SubmitField('Search')