from otree.api import *


doc = """
Second-Price Sealed Bid Auction (Session 4)
"""


class C(BaseConstants):
    NAME_IN_URL = 'second_price_auction'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
