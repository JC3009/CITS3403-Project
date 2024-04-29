from flask import render_template, redirect, url_for, flash
from app import flaskApp
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User

@flaskApp.route('/')
def home():
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

@flaskApp.route('/posting_request', methods=['GET'])
def posting_request():
    return render_template('posting_request.html')