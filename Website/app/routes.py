from flask import render_template
from app import flaskApp

@flaskApp.route('/')
def home():
    return render_template('index.html')
