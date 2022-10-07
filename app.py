from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "6uar1n0"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

boggle_game = Boggle()


@app.route("/")
def default_route():
    """default base template route and homepage"""

    homepage = True
    return render_template("index.html", homepage=homepage)


@app.route("/game")
def game_route():
    """route once game is started"""

    board = boggle_game.make_board()
    session['board'] = board

    return render_template("game.html", board=board)


@app.route("/wordcheck")
def word_check():
    """checking to see if word exists"""

    word = request.args["word"]
    board = session["board"]
    result = jsonify(boggle_game.check_valid_word(board, word))

    return result


@app.route("/score")
def score_update():
    """handling of scoring for game"""

    score = request.json["score"]

    return
