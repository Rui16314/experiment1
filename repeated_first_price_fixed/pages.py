from otree.api import *
from .models import *

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'session_type': 'fixed_matching'
        }

class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']
    timeout_seconds = C.BID_TIMEOUT

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.bid = -1

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        opponent = player.get_others_in_group()[0]
        
        player.opponent_valuation = opponent.valuation
        player.opponent_bid = opponent.bid
        
        # First-price auction logic
        if player.bid == -1:
            player.is_winner = False
            player.points = 0
        elif player.bid > opponent.bid:
            player.is_winner = True
            player.points = player.valuation - player.bid
        elif player.bid == opponent.bid:
            player.is_winner = True
            player.points = (player.valuation - player.bid) / 2
        else:
            player.is_winner = False
            player.points = 0
        
        return {
            'is_winner': player.is_winner,
            'points': player.points,
            'opponent_valuation': player.opponent_valuation,
            'opponent_bid': player.opponent_bid,
            'round_number': player.round_number,
            'total_rounds': C.NUM_ROUNDS
        }

page_sequence = [Introduction, Bid, Results]
