from flask import jsonify, redirect, render_template, request, session, url_for

from .services import newsDSA, weatherDSA, studyDSA, flashDSA

from . import app


@app.route('/')
def home():
    return render_template('home.html')

# community hub tools
# weather / arraylist + queue
@app.route("/weather")
def weather():
    return render_template("weather.html", locations=weatherDSA.LOCATIONS)


@app.route("/weather/api/check")
def weather_check():
    area = request.args.get("area", "Bacoor")
    return jsonify(weatherDSA.check_heat(area))

# news / linkedlist
@app.route('/news')
def news():
    category = request.args.get("category")
    return render_template('news.html', news_items=newsDSA.get_news(category), categories=newsDSA.CATEGORIES, category=category)

# study / queue
@app.route("/study")
def study():
    queue = studyDSA.from_list(session.get("study", []))
    items, total = studyDSA.with_schedule(queue.to_list())
    return render_template("study.html", now=items[0] if items else None, upcoming=items[1:], total=total)

@app.route("/study/add", methods=["POST"])
def study_add():
    subject = request.form.get("subject", "").strip()[:40]
    try:
        minutes = int(request.form.get("minutes", 25))
    except ValueError:
        minutes = 25
    minutes = max(1, min(minutes, 180))

    if subject:
        queue = studyDSA.from_list(session.get("study", []))
        queue.enqueue(subject, minutes)              
        session["study"] = queue.to_list()
    return redirect(url_for("study"))

@app.route("/study/next", methods=["POST"])
def study_next():
    queue = studyDSA.from_list(session.get("study", []))
    queue.dequeue()                                 
    session["study"] = queue.to_list()
    return redirect(url_for("study"))

# f;ashcards / linkedlist
@app.route("/flashcards")
def flashcards():
    cards = flashDSA.from_list(session.get("cards", [])).to_list()
    i = min(session.get("card_i", 0), max(len(cards) - 1, 0))
    return render_template("flashcards.html", card=cards[i] if cards else None, i=i, total=len(cards))

@app.route("/flashcards/add", methods=["POST"])
def flashcards_add():
    front = request.form.get("front", "").strip()[:60]
    back = request.form.get("back", "").strip()[:60]
    deck = flashDSA.from_list(session.get("cards", []))

    if front and back and deck.count < 20:
        if request.form.get("where") == "after":
            i = session.get("card_i", 0)
            deck.insert_after(i, front, back)     
            session["card_i"] = i + 1            
        else:
            deck.add_end(front, back)
        session["cards"] = deck.to_list()
    return redirect(url_for("flashcards"))

@app.route("/flashcards/move/<direction>")
def flashcards_move(direction):
    deck = flashDSA.from_list(session.get("cards", []))
    session["card_i"] = flashDSA.step(deck, session.get("card_i", 0), direction)
    return redirect(url_for("flashcards"))

@app.route("/flashcards/delete", methods=["POST"])
def flashcards_delete():
    deck = flashDSA.from_list(session.get("cards", []))
    i = session.get("card_i", 0)
    deck.delete(i)
    session["cards"] = deck.to_list()
    session["card_i"] = max(0, min(i, deck.count - 1))
    return redirect(url_for("flashcards"))




@app.route('/algorithms')
def algorithms():
    return render_template('algorithms.html')

@app.route('/binary-tree')
def binary_tree():
    return render_template('bn_tree.html')

@app.route('/graph')
def graph_maker():
    return render_template('graph.html')

@app.route('/maze')
def maze_maker():
    return render_template('maze.html')

@app.route('/simon')
def simon():
    return render_template('simon.html')

@app.route('/hanoi')
def hanoi():
    return render_template('hanoi.html')

