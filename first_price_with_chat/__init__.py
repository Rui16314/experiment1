from otree.api import *


doc = """
First-Price Auction with Communication (Session 3)
"""


class C(BaseConstants):
    NAME_IN_URL = 'first_price_with_chat'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
