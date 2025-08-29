from os import environ

SESSION_CONFIGS = [
    dict(
        name='first_price_auction',
        display_name="Session 1: First-Price Sealed Bid Auction",
        num_demo_participants=2,
        app_sequence=['first_price_auction'],
    ),
    dict(
        name='repeated_first_price_fixed',
        display_name="Session 2: Repeated First-Price Auction",
        num_demo_participants=2,
        app_sequence=['repeated_first_price_fixed'],
    ),
    dict(
        name='first_price_with_chat',
        display_name="Session 3: First-Price Auction with Chat",
        num_demo_participants=2,
        app_sequence=['first_price_with_chat'],
    ),
    dict(
        name='second_price_auction',
        display_name="Session 4: Second-Price Sealed Bid Auction",
        num_demo_participants=2,
        app_sequence=['second_price_auction'],
    ),
    dict(
        name='repeated_second_price_fixed',
        display_name="Session 5: Repeated Second-Price Auction",
        num_demo_participants=2,
        app_sequence=['repeated_second_price_fixed'],
    ),
    dict(
        name='second_price_with_chat',
        display_name="Session 6: Second-Price Auction with Chat",
        num_demo_participants=2,
        app_sequence=['second_price_with_chat'],
    ),
    dict(
        name='full_experiment',
        display_name="Full Experiment (All 6 Sessions)",
        num_demo_participants=2,
        app_sequence=[
            'first_price_auction',
            'repeated_first_price_fixed',
            'first_price_with_chat',
            'second_price_auction',
            'repeated_second_price_fixed',
            'second_price_with_chat',
            'results_dashboard'
        ],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['gender', 'age', 'race']
SESSION_FIELDS = []

# ISO-639 code
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ3310',
        display_name='ECON 3310 Experiment',
        participant_label_file='_rooms/econ3310.txt',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Welcome to the ECON 3310 Auction Experiment Platform
"""

SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']
