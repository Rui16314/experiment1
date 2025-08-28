from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'participation_fee': self.session.config.get('participation_fee', 0),
            'points': 100
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
        }


page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
