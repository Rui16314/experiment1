from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'Profile'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(
        label='What is your age?',
        min=18, max=100
    )
    
    gender = models.StringField(
        label='What is your gender?',
        choices=[
            ['Male', 'Male'],
            ['Female', 'Female'],
            ['Non-binary', 'Non-binary'],
            ['Prefer not to say', 'Prefer not to say']
        ],
        widget=widgets.RadioSelect
    )
    
    race = models.StringField(
        label='What is your race/ethnicity?',
        choices=[
            ['White', 'White'],
            ['Black or African American', 'Black or African American'],
            ['Hispanic or Latino', 'Hispanic or Latino'],
            ['Asian', 'Asian'],
            ['Native American', 'Native American'],
            ['Other', 'Other'],
            ['Prefer not to say', 'Prefer not to say']
        ],
        widget=widgets.RadioSelect
    )
    
    major = models.StringField(
        label='What is your major?',
        choices=[
            ['Economics', 'Economics'],
            ['Business', 'Business'],
            ['STEM', 'STEM'],
            ['Social Sciences', 'Social Sciences'],
            ['Humanities', 'Humanities'],
            ['Other', 'Other']
        ]
    )
