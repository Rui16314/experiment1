from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'session_number': 3,
            'session_title': 'First-Price Auction with Communication'
        }


class ChatPage(Page):
    timeout_seconds = 60
    form_model = 'player'
    
    def is_displayed(self):
        return self.round_number <= Constants.num_rounds
    
    def vars_for_template(self):
        # Get chat messages for display
        chat_messages = self.group.get_chat_messages()
        return {
            'chat_messages': chat_messages,
            'player_id': self.player.id_in_group,
            'round_number': self.round_number
        }
    
    def live_method(self, data):
        # Handle real-time chat messages
        if data['type'] == 'chat_message':
            self.group.add_chat_message(data['message'], self.player.id_in_group)
            # Return updated messages to all players in group
            return {
                0: dict(
                    type='chat_update',
                    messages=self.group.get_chat_messages()
                )
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


page_sequence = [Introduction, ChatPage, Bid, ResultsWaitPage, Results]
