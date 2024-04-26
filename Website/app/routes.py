from flask import render_template, redirect, url_for, flash
from app import flaskApp
from app.forms import LoginForm
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