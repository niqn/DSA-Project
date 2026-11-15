import random
from flask import jsonify, redirect, render_template, request, session, url_for

from .services import newsDSA, weatherDSA, studyDSA, flashDSA

from . import app
from .services.algorithms import bubble_sort, insertion_sort, linear_search, binary_search, calculate_number_theory, NUMBER_THEORY_METADATA
from .services.binary_tree import BinaryTree


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



@app.route('/algorithms', methods=['GET'])
def algorithms():
    return render_template('algorithms.html', formulas=NUMBER_THEORY_METADATA)


@app.route('/algorithms/steps', methods=['POST'])
def algorithm_steps():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request data"}), 400

    algorithm = data.get("algorithm")

    # Generate or reuse array
    if "array" in data:
        arr = data["array"]

        if not isinstance(arr, list) or not all(type(x) is int for x in arr):
            return jsonify({"error": "Invalid array"}), 400

        if not 5 <= len(arr) <= 50:
            return jsonify({"error": "Invalid array size"}), 400

    else:
        size = data.get("size", 10)

        if type(size) is not int or not 5 <= size <= 50:
            return jsonify({"error": "Invalid array size"}), 400

        arr = [random.randint(5, 100) for _ in range(size)]

    original_array = arr.copy()
    display_array = arr.copy()

    # Sorting
    if algorithm == "bubble":
        steps = bubble_sort(arr.copy())

    elif algorithm == "insertion":
        steps = insertion_sort(arr.copy())

    # Searching
    elif algorithm in ("linear", "binary"):
        target = data.get("target")

        if type(target) is not int:
            return jsonify({"error": "Invalid target"}), 400

        if algorithm == "linear":
            steps = linear_search(display_array.copy(), target)

        else:
            display_array.sort()
            steps = binary_search(display_array.copy(), target)

    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    return jsonify({
        "original_array": original_array,
        "display_array": display_array,
        "steps": steps
    })

@app.route("/algorithms/number-theory", methods=["POST"])
def number_theory():
    data = request.get_json(silent=True) or {}

    operation = data.get("operation")
    values = data.get("values", {})

    if not isinstance(operation, str):
        return jsonify({
            "success": False,
            "error": "Please select a valid operation."
        }), 400

    if not isinstance(values, dict):
        return jsonify({
            "success": False,
            "error": "Invalid input values."
        }), 400

    try:
        result = calculate_number_theory(operation, values)

        return jsonify({
            "success": True,
            "result": result
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

@app.route('/binary-tree')
def binary_tree():
    # Start a fresh tree whenever the page is opened/reloaded
    session["binary_tree"] = {
        "root": None,
        "next_id": 0
    }

    return render_template('bn_tree.html')

def get_binary_tree():
    state = session.get("binary_tree")
    return BinaryTree.from_state(state)


def save_binary_tree(tree):
    session["binary_tree"] = tree.to_state()

# GET TREE
@app.route('/binary-tree/data', methods=['GET'])
def binary_tree_data():
    tree = get_binary_tree()

    return jsonify({
        "tree": tree.to_dict()
    })


# CREATE ROOT
@app.route('/binary-tree/create', methods=['POST'])
def binary_tree_create():
    data = request.get_json(silent=True) or {}
    value = data.get("data")

    if value is None or str(value).strip() == "":
        return jsonify({"error": "Enter a node value."}), 400

    tree = get_binary_tree()

    result = tree.create_root(value)

    if isinstance(result, str):
        return jsonify({"error": result}), 400

    save_binary_tree(tree)

    return jsonify({
        "tree": tree.to_dict()
    })


# ADD NODE
@app.route('/binary-tree/add', methods=['POST'])
def binary_tree_add():
    data = request.get_json(silent=True) or {}

    parent_id = data.get("parent_id")
    value = data.get("data")
    side = data.get("side")

    if type(parent_id) is not int:
        return jsonify({"error": "Invalid parent ID."}), 400

    if value is None or str(value).strip() == "":
        return jsonify({"error": "Enter a node value."}), 400

    tree = get_binary_tree()

    result = tree.add(parent_id, value, side)

    if isinstance(result, str):
        return jsonify({"error": result}), 400

    save_binary_tree(tree)

    return jsonify({
        "tree": tree.to_dict()
    })


# DELETE NODE
@app.route('/binary-tree/delete', methods=['POST'])
def binary_tree_delete():
    data = request.get_json(silent=True) or {}
    node_id = data.get("node_id")

    if type(node_id) is not int:
        return jsonify({"error": "Invalid node ID."}), 400

    tree = get_binary_tree()

    result = tree.delete(node_id)

    if isinstance(result, str):
        return jsonify({"error": result}), 400

    save_binary_tree(tree)

    return jsonify({
        "tree": tree.to_dict()
    })


# TRAVERSAL
@app.route('/binary-tree/traverse', methods=['POST'])
def binary_tree_traverse():
    data = request.get_json(silent=True) or {}
    method = data.get("method", "inorder")

    tree = get_binary_tree()

    if tree.root is None:
        return jsonify({"error": "Tree is empty."}), 400

    result = tree.traverse(method)

    if isinstance(result, str):
        return jsonify({"error": result}), 400

    return jsonify({
        "steps": result,
        "method": method
    })


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

