from flask import render_template
from app import flaskApp
from app.forms import LoginForm

@flaskApp.route('/')
def home():
    return render_template('page_main.html')

@flaskApp.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
