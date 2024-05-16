from flask import render_template, redirect, url_for, flash
from app import flaskApp
from app.forms import LoginForm, RegistrationForm, JobRequestForm, TradieUserForm, JobOfferForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, JobRequest, TradieUser, JobOffer

@flaskApp.route('/')
def home():
    recent_jobs = db.session.scalars(sa.select(JobRequest).order_by(JobRequest.datetimeCreated.desc()).limit(4))
    return render_template('page_main.html', jobs=recent_jobs)

@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash(f'Logged in successfully. User: {current_user.username}')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@flaskApp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@flaskApp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@login_required
@flaskApp.route('/posting_request', methods=['GET', 'POST'])
def posting_request():
    user_id = int(current_user.id)
    form = JobRequestForm()
    if form.validate_on_submit():
        jobRequest = JobRequest(
            streetNumber=form.streetNumber.data, 
            street=form.street.data, 
            suburb=form.suburb.data, 
            postcode=form.postcode.data, 
            state=form.state.data,
            user_id=user_id,
            tradeRequired=form.tradeRequired.data, 
            job=form.title.data, 
            description=form.description.data)
        db.session.add(jobRequest)
        db.session.commit()
        flash(f'Job request posted!')
        return redirect(url_for('home'))
    return render_template('posting_request.html', form=form)

@login_required
@flaskApp.route('/tradie_register', methods=['GET', 'POST'])
def tradie_register():
    user_id = int(current_user.id)
    #check if user has tradie account associated with them already
    existing_tradie = db.session.query(TradieUser).filter_by(user_id=user_id).first()
    #if they do, redirect them to home page
    if existing_tradie:
        flash('You have already registered as a tradie!')
        return redirect(url_for('home'))
    form = TradieUserForm()
    if form.validate_on_submit():
        tradie = TradieUser(
            user_id=user_id, 
            trade=form.trade.data, 
            hourlyRate=form.hourlyRate.data, 
            calloutFee=form.calloutFee.data)
        db.session.add(tradie)
        db.session.commit()
        flash(f'Tradie details registered!')
        return redirect(url_for('home'))
    return render_template('tradie_register.html', form=form)

@login_required
@flaskApp.route('/view_request/<request_id>')
def view_request(request_id):
    jobRequest = db.session.scalar(sa.select(JobRequest).where(JobRequest.id == int(request_id)))
    offers = db.session.scalars(sa.select(JobOffer).where(JobOffer.jobRequest_id == jobRequest.id)).all()
    return render_template('view_request.html', job_request=jobRequest, offers=offers)

@login_required
@flaskApp.route('/offer_services/<request_id>', methods=['GET', 'POST'])
def offer_services(request_id):
    tradie_user_id = int(current_user.id)
    tradie_tradie_id = db.session.scalar(sa.select(TradieUser.id).where(TradieUser.user_id == tradie_user_id))
    #check if user is a tradie
    existing_tradie = db.session.query(TradieUser).filter_by(user_id=tradie_user_id).first()
    #if they are not, redirect them to home page
    if not existing_tradie:
        flash('Only tradies can offer services!')
        return redirect(url_for('home'))
    jobRequest = db.session.scalar(sa.select(JobRequest).where(JobRequest.id == int(request_id)))
    #don't allow tradies to offer services for jobs they are not qualified for
    if existing_tradie.trade != jobRequest.tradeRequired:
        flash(f'You are not qualified to offer services for a job that requires a {jobRequest.tradeRequired}!')
        return redirect(url_for('home'))
    form = JobOfferForm()
    if form.validate_on_submit():
        job_offer = JobOffer(
            timeEstimate=form.timeEstimate.data,
            dateOffered=form.dateOffered.data,
            jobRequest_id=jobRequest.id,
            tradie_id=tradie_tradie_id
        )
        db.session.add(job_offer)
        db.session.commit()
        flash('Job Offer has been created!')
        return redirect(url_for('home'))
    return render_template('offer_services.html', job_request=jobRequest, form=form)