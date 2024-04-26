from flask import render_template
from app import flaskApp

@flaskApp.route('/')
def home():
    return render_template('page_main.html')

@flaskApp.route('/login')
def login():
    return render_template('login.html')
