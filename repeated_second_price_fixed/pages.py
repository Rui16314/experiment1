from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'session_number': 5,
            'session_title': 'Repeated Second-Price Auction'
        }


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.bid_amount = 0


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        return {
            'is_winner': self.player.is_winner,
            'opponent_bid': self.player.other_player().bid_amount,
            'opponent_valuation': self.player.other_player().private_value,
            'round_number': self.round_number,
            'total_rounds': Constants.num_rounds,
            'cumulative_payoff': self.participant.payoff_plus_participation_fee()
        }


page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
