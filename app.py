from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Constants
NUM_EXPERIMENTS = 6
ROUNDS_PER_EXPERIMENT = 10

# Database setup
def init_db():
    conn = sqlite3.connect('auction.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            experiment INTEGER,
            round INTEGER,
            valuation REAL,
            bid REAL,
            opponent TEXT,
            opponent_bid REAL,
            winner TEXT,
            winning_bid REAL,
            price_paid REAL,
            payoff REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
        return redirect(url_for('round'))
    return render_template('login.html')

@app.route('/round', methods=['GET', 'POST'])
def round():
    name = session.get('name')
    experiment = session.get('experiment', 1)
    round_number = session.get('round', 1)

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

        # Determine actual winner name
        winner_name = name if winner == 'player1' else opponent if winner == 'player2' else 'None'
        payoff = payoff1 if winner == 'player1' else payoff2 if winner == 'player2' else 0

        # Store result
        conn = sqlite3.connect('auction.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO results (name, experiment, round, valuation, bid, opponent, opponent_bid,
                                 winner, winning_bid, price_paid, payoff)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, experiment, round_number, valuation, bid, opponent, opponent_bid,
              winner_name, winning_bid, price_paid, payoff))
        conn.commit()
        conn.close()

        return redirect(url_for('round_result'))

    return render_template('round.html', round_number=round_number, valuation=valuation)

@app.route('/round_result')
def round_result():
    name = session.get('name')
    experiment = session.get('experiment')
    round_number = session.get('round')

    conn = sqlite3.connect('auction.db')
    c = conn.cursor()
    c.execute('''
        SELECT valuation, bid, opponent, opponent_bid, winner, winning_bid, price_paid, payoff
        FROM results
        WHERE name = ? AND experiment = ? AND round = ?
    ''', (name, experiment, round_number))
    result = c.fetchone()
    conn.close()

    session['round'] += 1
    if session['round'] > ROUNDS_PER_EXPERIMENT:
        session['experiment'] += 1
        session['round'] = 1

    return render_template('round_result.html',
                           round_number=round_number,
                           winner=result[4],
                           winning_bid=result[5],
                           user_bid=result[1],
                           price_paid=result[6],
                           payoff=result[7],
                           opponent=result[2],
                           opponent_bid=result[3])

@app.route('/results')
def results():
    conn = sqlite3.connect('auction.db')
    c = conn.cursor()
    c.execute('SELECT experiment, name, SUM(payoff) FROM results GROUP BY experiment, name')
    earnings = c.fetchall()
    conn.close()

    results_dict = {}
    for exp, name, total in earnings:
        if exp not in results_dict:
            results_dict[exp] = {}
        results_dict[exp][name] = round(total, 2)

    return render_template('results.html', results=results_dict)

# Live chat
@socketio.on('chat_message')
def handle_chat_message(msg):
    name = session.get('name', 'Anonymous')
    emit('chat_message', f"{name}: {msg}", broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)
