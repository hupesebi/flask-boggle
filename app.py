from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

boggle_game = Boggle()

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board = board)

@app.route('/checkword')
def check_word():
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result' : response})

@app.route('/score', methods=['POST'])
def save_score():
    score = request.json['score']
    highscore = session.get('highscore', 0)
    times_played = session.get('times-played', 0)
    session['times-played'] = times_played +1
    session['highscore'] = max(score, highscore)
    return jsonify({'highscore' : highscore})

