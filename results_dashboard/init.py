from otree.api import *

doc = """
Results dashboard showing experiment data and comparisons
"""

class C(BaseConstants):
    NAME_IN_URL = 'results_dashboard'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
