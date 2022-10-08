from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "6uar1n0"

boggle_game = Boggle()


@app.route("/")
def default_route():
    """default base template route and homepage"""

    homepage = True
    
    return render_template("index.html", homepage=homepage)


@app.route("/game")
def game_route():
    """main game route to setup game board and session variables"""

    board = boggle_game.make_board()
    session["board"] = board
    numplays = session.get("numplays", 0)
    highscore = session.get("highscore", 0)
    
    return render_template("game.html", board=board, numplays=numplays, highscore=highscore)


@app.route("/wordcheck")
def word_check():
    """checking to see if word exists and return result"""

    word = request.args["word"]
    board = session["board"]
    result = jsonify(boggle_game.check_valid_word(board, word))

    return result


@app.route("/score", methods=["POST"])
def score_update():
    """handling of scoring for game and stats, checks if highscore was hit or not too"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    session["numplays"] = numplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
