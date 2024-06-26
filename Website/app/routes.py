from flask import render_template, redirect, url_for, flash
from app.blueprints import main as flaskApp
from app.forms import LoginForm, RegistrationForm, JobRequestForm, TradieUserForm, JobOfferForm, RespondToOfferForm, RequestSearchForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, JobRequest, TradieUser, JobOffer
from app.controllers import login_user_controller, LoginError, existing_tradie_controller, TradieExistsError, TradieNotExistsError, compare_trade_controller, TradeError, job_request_controller, JobRequestError

@flaskApp.route('/')
def home():
    recent_jobs = db.session.scalars(sa.select(JobRequest).order_by(JobRequest.datetimeCreated.desc()).limit(4))
    return render_template('page_main.html', jobs=recent_jobs)

@flaskApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        try:
            login_user_controller(user, form.password.data)
            login_user(user)
            flash(f'Logged in successfully. User: {current_user.username}')
            return redirect(url_for('main.home'))
        except LoginError as e:
            flash(str(e))
            return redirect(url_for('main.login'))   
    return render_template('login.html', form=form)

@flaskApp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@flaskApp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@flaskApp.route('/posting_request', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.home'))
    return render_template('posting_request.html', form=form)

@flaskApp.route('/tradie_register', methods=['GET', 'POST'])
@login_required
def tradie_register():
    user_id = int(current_user.id)
    #check if user has tradie account associated with them already
    existing_tradie = db.session.query(TradieUser).filter_by(user_id=user_id).first()
    #if they do, redirect them to home page
    try:
        existing_tradie_controller(user_id)
    except TradieExistsError as e:
        flash(str(e))
        return redirect(url_for('main.home'))
    except TradieNotExistsError:
        pass
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
        return redirect(url_for('main.home'))
    return render_template('tradie_register.html', form=form)

@flaskApp.route('/view_request/<request_id>')
@login_required
def view_request(request_id):
    jobRequest = db.session.scalar(sa.select(JobRequest).where(JobRequest.id == int(request_id)))
    offers = db.session.scalars(sa.select(JobOffer).where(JobOffer.jobRequest_id == jobRequest.id)).all()
    return render_template('view_request.html', job_request=jobRequest, offers=offers)

@flaskApp.route('/offer_services/<request_id>', methods=['GET', 'POST'])
@login_required
def offer_services(request_id):
    tradie_user_id = int(current_user.id)
    tradie_tradie_id = db.session.scalar(sa.select(TradieUser.id).where(TradieUser.user_id == tradie_user_id))
    try:
        existing_tradie_controller(tradie_user_id)
    except TradieNotExistsError as e:
        flash(str(e))
        return redirect(url_for('main.home'))
    except TradieExistsError:
        pass
    jobRequest = db.session.scalar(sa.select(JobRequest).where(JobRequest.id == int(request_id)))
    tradie = db.session.scalar(sa.select(TradieUser).where(TradieUser.id == tradie_tradie_id))
    try:
        compare_trade_controller(tradie.trade, jobRequest.tradeRequired)
    except TradeError as e:    
        flash(str(e))
        return redirect(url_for('main.home'))
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
        return redirect(url_for('main.home'))
    return render_template('offer_services.html', job_request=jobRequest, form=form)

@flaskApp.route('/respond_to_offer/<offer_id>', methods=['GET','POST'])
@login_required
def respond_to_offer(offer_id):
    form = RespondToOfferForm()
    job_offer = db.session.scalar(sa.select(JobOffer).where(JobOffer.id == int(offer_id)))
    #check if user is the creator of the job request associated with the offer
    try:
        job_request_controller(job_offer.jobRequest.user_id, int(current_user.id), job_offer.acceptedStatus, job_offer.rejectedStatus)
    except JobRequestError as e:
        flash(str(e))
        return redirect(url_for('main.view_request', request_id=job_offer.jobRequest.id))
    if form.validate_on_submit() and not (job_offer.acceptedStatus or job_offer.rejectedStatus):
        if form.response.data == 'accept':
            job_offer.acceptedStatus = True
            db.session.commit()
            flash('Job Offer has been accepted!')
            return redirect(url_for('main.home'))
        elif form.response.data == 'reject':
            job_offer.rejectedStatus = True
            db.session.commit()
            flash('Job Offer has been rejected!')
            return redirect(url_for('main.home'))

    return render_template('respond_to_offer.html', offer=job_offer, form=form)

@flaskApp.route('/request_history')
@login_required
def request_history():
    user_id = int(current_user.id)
    user_requests = db.session.scalars(sa.select(JobRequest).where(JobRequest.user_id == user_id)).all()
    return render_template('request_history.html', requests=user_requests)

@flaskApp.route('/offer_history')
@login_required
def offer_history():
    tradie_user_id = int(current_user.id)
    tradie_tradie_id = db.session.scalar(sa.select(TradieUser.id).where(TradieUser.user_id == tradie_user_id))
    try:
        existing_tradie_controller(tradie_user_id)
    except TradieNotExistsError as e:
        flash(str(e))
        return redirect(url_for('main.home'))
    except TradieExistsError:
        pass
    user_offers = db.session.scalars(sa.select(JobOffer).where(JobOffer.tradie_id == tradie_tradie_id)).all()
    return render_template('offer_history.html', offers=user_offers)

@flaskApp.route('/search_requests', methods=['GET', 'POST'])
@login_required
def search_requests():
    form = RequestSearchForm()
    if form.validate_on_submit():
        search = db.session.query(JobRequest)
        if form.tradeFilter.data != 'all':
            search = search.filter(JobRequest.tradeRequired == form.tradeFilter.data)
        if form.stateFilter.data != 'all':
            search = search.filter(JobRequest.state == form.stateFilter.data)
        if form.postcodeFilter.data != '':
            search = search.filter(JobRequest.postcode == form.postcodeFilter.data)
        if form.order.data == 'datetimeCreated':
            search = search.order_by(JobRequest.datetimeCreated.desc())
        elif form.order.data == 'job':
            search = search.order_by(JobRequest.job)
        elif form.order.data == 'state':
            search = search.order_by(JobRequest.state)
        elif form.order.data == 'postcode':
            search = search.order_by(JobRequest.postcode)
        search_results = search.all()
        return render_template('search_requests.html', form=form, requests=search_results)
    return render_template('search_requests.html', form=form, requests=None)

@flaskApp.route('/edit_request/<request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    user_id = int(current_user.id)
    jobRequest = db.session.scalar(sa.select(JobRequest).where(JobRequest.id == int(request_id)))
    try:
        job_request_controller(jobRequest.user_id, user_id, False, False)
    except JobRequestError as e:
        flash(str(e))
        return redirect(url_for('main.view_request', request_id=request_id))
    form = JobRequestForm()
    if form.validate_on_submit() and jobRequest.user_id == user_id:
        updated_request_data = {
            'streetNumber':form.streetNumber.data,
            'street':form.street.data,
            'suburb':form.suburb.data,
            'postcode':form.postcode.data,
            'state':form.state.data,
            'tradeRequired':form.tradeRequired.data,
            'job':form.title.data,
            'description':form.description.data
        }
        db.session.query(JobRequest).filter(JobRequest.id == request_id).update(updated_request_data)
        flash('Job Request has been updated!')
        return redirect(url_for('main.view_request', request_id=request_id))
    return render_template('edit_request.html', form=form)