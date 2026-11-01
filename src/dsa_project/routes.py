from flask import render_template

from . import app

@app.route('/')
def index():
    return "hello"

@app.route('/weather')
def weather():
    return render_template('weather.html')