from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
from firebase_setup import db
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Constants
NUM_EXPERIMENTS = 6
ROUNDS_PER_EXPERIMENT = 10

# Valuation generator
def generate_valuation():
    return round(random.randint(0, 10000) / 100, 2)

# Bot strategy
def bot_bid(exp_type, valuation):
    if exp_type in [1, 2, 3]:  # First-price
        return round(valuation / 2, 2)
    else:  # Second-price
        return valuation

# Auction logic
def resolve_auction(exp_type, v1, b1, v2, b2):
    if b1 > b2:
        winner = 'player1'
        winning_bid = b1
        price_paid = b1 if exp_type in [1, 2, 3] else b2
        payoff1 = v1 - price_paid if b1 != v1 else 0
        payoff2 = 0
    elif b2 > b1:
        winner = 'player2'
        winning_bid = b2
        price_paid = b2 if exp_type in [1, 2, 3] else b1
        payoff2 = v2 - price_paid if b2 != v2 else 0
        payoff1 = 0
    else:
        winner = 'tie'
        winning_bid = b1
        price_paid = 0
        payoff1 = payoff2 = 0
    return winner, winning_bid, price_paid, payoff1, payoff2

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['experiment'] = 1
        session['round'] = 1
        return redirect(url_for('play_round'))
    return render_template('login.html')

@app.route('/round', methods=['GET', 'POST'])
def play_round():
    name = session.get('name')
    experiment = session.get('experiment', 1)
    round_number = int(session.get('round', 1))

    if experiment > NUM_EXPERIMENTS:
        return redirect(url_for('results'))

    valuation = generate_valuation()
    session['valuation'] = valuation

    if request.method == 'POST':
        bid = request.form.get('bid')
        bid = float(bid) if bid else bot_bid(experiment, valuation)
        session['bid'] = bid

        # Simulate opponent
        opponent = 'Bot'
        opponent_valuation = generate_valuation()
        opponent_bid = bot_bid(experiment, opponent_valuation)

        # Resolve auction
        winner, winning_bid, price_paid, payoff1, payoff2 = resolve_auction(
            experiment, valuation, bid, opponent_valuation, opponent_bid
        )

        winner_name = name if winner == 'player1' else opponent if winner == 'player2' else 'None'
        payoff = payoff1 if winner == 'player1' else payoff2 if winner == 'player2' else 0

        # Store result in Firebase
        db.collection('results').add({
            'name': name,
            'experiment': experiment,
            'round': round_number,
            'valuation': valuation,
            'bid': bid,
            'opponent': opponent,
            'opponent_bid': opponent_bid,
            'winner': winner_name,
            'winning_bid': winning_bid,
            'price_paid': price_paid,
            'payoff': payoff,
            'timestamp': datetime.utcnow()
        })

        return redirect(url_for('round_result'))

    return render_template('round.html',
                           round_number=round_number,
                           valuation=valuation,
                           experiment=experiment)

@app.route('/round_result')
def round_result():
    name = session.get('name')
    experiment = session.get('experiment')
    round_number = int(session.get('round', 1))

    result_ref = db.collection('results') \
        .where('name', '==', name) \
        .where('experiment', '==', experiment) \
        .where('round', '==', round_number) \
        .limit(1).stream()

    result = next(result_ref, None)
    data = result.to_dict() if result else {}

    session['round'] += 1
    if session['round'] > ROUNDS_PER_EXPERIMENT:
        session['experiment'] += 1
        session['round'] = 1

    return render_template('round_result.html',
                           round_number=round_number,
                           winner=data.get('winner'),
                           winning_bid=data.get('winning_bid'),
                           user_bid=data.get('bid'),
                           price_paid=data.get('price_paid'),
                           payoff=data.get('payoff'),
                           opponent=data.get('opponent'),
                           opponent_bid=data.get('opponent_bid'))

@app.route('/results')
def results():
    results = db.collection('results').stream()
    earnings = {}

    for doc in results:
        data = doc.to_dict()
        exp = data['experiment']
        name = data['name']
        payoff = data['payoff']

        earnings.setdefault(exp, {}).setdefault(name, 0)
        earnings[exp][name] += payoff

    for exp in earnings:
        for name in earnings[exp]:
            earnings[exp][name] = round(earnings[exp][name], 2)

    return render_template('results.html', results=earnings)

# Live chat
@socketio.on('chat_message')
def handle_chat_message(msg):
    name = session.get('name', 'Anonymous')
    emit('chat_message', f"{name}: {msg}", broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)

