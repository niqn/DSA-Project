from flask import render_template, request
from .services import newsDSA

from . import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/weather')
def weather():
    return render_template('weather.html')


@app.route('/news')
def news():
    category = request.args.get("category")
    return render_template('news.html', news_items=newsDSA.get_news(category), categories=newsDSA.CATEGORIES, category=category)

@app.route('/generators')#qr, password, etc.
def gen():
    return render_template('generators.html')

@app.route('/random')#rng, coin flip, dice, wheel, etc.
def random():
    return render_template('random.html')

@app.route('/time')#timer, stopwatch
def time():
    return render_template('time.html')

@app.route('/text')#word counter, unique words, alphabetical sorter, etc.
def text():
    return render_template('text.html')

@app.route('/games')#idk
def game():
    return render_template('game.html')

