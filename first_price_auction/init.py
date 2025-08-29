from otree.api import *

doc = """
First-price sealed bid auction with random matching
"""

class C(BaseConstants):
    NAME_IN_URL = 'first_price_auction'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    VALUATION_MIN = 0
    VALUATION_MAX = 100
    BID_TIMEOUT = 60  # 1 minute

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    valuation = models.FloatField(min=0, max=100)
    bid = models.FloatField(min=0, max=100)
    is_winner = models.BooleanField(initial=False)
    points = models.FloatField(initial=0)
    opponent_valuation = models.FloatField()
    opponent_bid = models.FloatField()
