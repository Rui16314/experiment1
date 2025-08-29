from otree.api import *


doc = """
ECON 3310 Auction Experiment Platform
"""


class C(BaseConstants):
    NAME_IN_URL = 'econ3310_auction_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGE SEQUENCE
page_sequence = [Page]
