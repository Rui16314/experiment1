from otree.api import *


doc = """
Repeated Second-Price Auction (Session 5)
"""


class C(BaseConstants):
    NAME_IN_URL = 'repeated_second_price_fixed'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
