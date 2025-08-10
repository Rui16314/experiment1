from firebase_setup import db
from datetime import datetime

def start_round(pair, item):
    round_ref = db.collection('auction_rounds').document()
    round_ref.set({
        'players': pair,
        'item': item,
        'start_time': datetime.utcnow(),
        'status': 'active'
    })
    return round_ref.id

def submit_bid(round_id, player, bid_amount):
    bid_ref = db.collection('auction_rounds').document(round_id).collection('bids')
    bid_ref.add({
        'player': player,
        'amount': bid_amount,
        'timestamp': datetime.utcnow()
    })

def get_highest_bid(round_id):
    bid_ref = db.collection('auction_rounds').document(round_id).collection('bids')
    bids = bid_ref.order_by('amount', direction='DESCENDING').limit(1).stream()
    return next(bids, None)
