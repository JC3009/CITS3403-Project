from flask import render_template, redirect, url_for, flash
from app import flaskApp
from app.forms import LoginForm, RegistrationForm, JobRequestForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, JobRequest

@flaskApp.route('/')
def home():
    #recent_jobs = db.session.scalars(sa.select(JobRequest).order_by(JobRequest.timestamp.desc()).limit(4))
    return render_template('page_main.html')

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
            job=form.title.data, 
            description=form.description.data)
        db.session.add(jobRequest)
        db.session.commit()
        flash(f'Job request posted!')
        return redirect(url_for('home'))
    return render_template('posting_request.html', form=form)
