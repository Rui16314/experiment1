from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import json


class Constants(BaseConstants):
    name_in_url = 'first_price_with_chat'
    players_per_group = 2
    num_rounds = 10

    instructions_template = 'first_price_with_chat/Instructions.html'
    min_valuation = 0
    max_valuation = 100
    step_valuation = 0.01


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            # Randomly pair players and keep them together for all rounds
            self.group_randomly()
        else:
            # Keep the same groups as previous round
            self.group_like_round(1)


class Group(BaseGroup):
    chat_messages = models.LongStringField(initial="[]")
    highest_bid = models.CurrencyField()
    winning_bid = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        bids = [p.bid_amount for p in players]
        self.highest_bid = max(bids)
        
        # Check for tie
        if bids[0] == bids[1]:
            # In case of tie, split the payoff
            for p in players:
                if p.bid_amount == self.highest_bid:
                    p.payoff = (p.private_value - p.bid_amount) / 2
                    p.is_winner = True
                else:
                    p.payoff = 0
                    p.is_winner = False
        else:
            winner = None
            for p in players:
                if p.bid_amount == self.highest_bid:
                    winner = p
                    break
            
            for p in players:
                if p == winner:
                    p.payoff = p.private_value - p.bid_amount
                    p.is_winner = True
                else:
                    p.payoff = 0
                    p.is_winner = False
        
        self.winning_bid = self.highest_bid

    def get_chat_messages(self):
        try:
            return json.loads(self.chat_messages)
        except:
            return []

    def add_chat_message(self, message, player_id):
        messages = self.get_chat_messages()
        messages.append({
            'player_id': player_id,
            'message': message,
            'round_number': self.round_number
        })
        self.chat_messages = json.dumps(messages)
        self.save()


class Player(BasePlayer):
    private_value = models.CurrencyField(
        min=Constants.min_valuation,
        max=Constants.max_valuation,
        doc="Private value of the item for this player"
    )
    
    bid_amount = models.CurrencyField(
        min=0,
        max=Constants.max_valuation,
        doc="Amount bid by the player",
        label="Please enter your bid (0 - 100):"
    )
    
    is_winner = models.BooleanField(
        initial=False,
        doc="Indicates whether the player won the auction"
    )

    def generate_private_value(self):
        # Generate random value between min and max with specified step
        range_size = int((Constants.max_valuation - Constants.min_valuation) / Constants.step_valuation) + 1
        random_index = random.randint(0, range_size - 1)
        value = Constants.min_valuation + random_index * Constants.step_valuation
        return value

    def role(self):
        return {1: 'Player 1', 2: 'Player 2'}[self.id_in_group]
