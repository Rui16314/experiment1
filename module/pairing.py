import random
from firebase_setup import db

def get_active_players():
    players_ref = db.collection('players')
    docs = players_ref.where('status', '==', 'waiting').stream()
    return [doc.id for doc in docs]

def pair_players():
    players = get_active_players()
    random.shuffle(players)
    pairs = [(players[i], players[i+1]) for i in range(0, len(players)-1, 2)]
    return pairs
