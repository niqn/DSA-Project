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
