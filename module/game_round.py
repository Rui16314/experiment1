from firebase_setup import db
from datetime import datetime

def start_round(pair, item):
    """
    Creates a new auction round with two players and an item.

    Args:
        pair (list): List of two player identifiers.
        item (str): Item being auctioned.

    Returns:
        str: The unique round ID.
    """
    round_ref = db.collection('auction_rounds').document()
    round_ref.set({
        'players': pair,
        'item': item,
        'start_time': datetime.utcnow(),
        'status': 'active'
    })
    return round_ref.id

def submit_bid(round_id, player, bid_amount):
    """
    Submits a bid to the specified auction round.

    Args:
        round_id (str): ID of the auction round.
        player (str): Player submitting the bid.
        bid_amount (float): Bid amount.
    """
    bid_ref = db.collection('auction_rounds').document(round_id).collection('bids')
    bid_ref.add({
        'player': player,
        'amount': bid_amount,
        'timestamp': datetime.utcnow()
    })

def get_highest_bid(round_id):
    """
    Retrieves the highest bid in the auction round.

    Args:
        round_id (str): ID of the auction round.

    Returns:
        dict or None: Highest bid data or None if no bids exist.
    """
    bid_ref = db.collection('auction_rounds').document(round_id).collection('bids')
    bids = bid_ref.order_by('amount', direction='DESCENDING').limit(1).stream()
    highest = next(bids, None)
    if highest:
        return {
            'player': highest.get('player'),
            'amount': highest.get('amount'),
            'timestamp': highest.get('timestamp')
        }
    return None
