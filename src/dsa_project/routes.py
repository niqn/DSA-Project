from flask import jsonify, redirect, render_template, request, session, url_for
from .services import newsDSA, weatherDSA, emergencyDSA

from . import app


@app.route('/')
def home():
    return render_template('home.html')

# community hub tools
@app.route("/weather")
def weather():
    return render_template("weather.html", locations=weatherDSA.LOCATIONS)


@app.route("/weather/api/check")
def weather_check():
    area = request.args.get("area", "Bacoor")
    return jsonify(weatherDSA.check_heat(area))


@app.route('/news')
def news():
    category = request.args.get("category")
    return render_template('news.html', news_items=newsDSA.get_news(category), categories=newsDSA.CATEGORIES, category=category)


@app.route('/emergency')
def emergency():
    city = request.args.get("city", "Bacoor")
    barangay = request.args.get("barangay", "")
    category = request.args.get("category", "")
    q = request.args.get("q", "")

    session["recent"] = emergencyDSA.remember_search(session.get("recent", []), q)

    return render_template(
        "emergency.html",
        results=emergencyDSA.search(city, barangay, category, q),
        cities=emergencyDSA.CITIES, barangays=emergencyDSA.BARANGAYS,
        categories=emergencyDSA.CATEGORIES,
        recent=session["recent"],
        city=city, barangay=barangay, category=category, q=q,
    )


@app.route('/emergency/undo')
def emergency_undo():
    # stack: pop the newest search
    session["recent"] = emergencyDSA.forget_last(session.get("recent", []))
    return redirect(url_for('emergency'))

# quick? tools
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

