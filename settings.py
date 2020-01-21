from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=0.00, doc=""
)


SESSION_CONFIGS = [
    dict(name='prisoner',
	display_name="Prisoner's Dilemma", 
	num_demo_participants=2,
	app_sequence=['validation', 'prisoner', 'survey', 'payment_info']),
]

environ["OTREE_AUTH_LEVEL"] = "STUDY"

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(name='pd_stakes',
	display_name='Repeated PD with changing stakes based on past behavior')
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

RECAPTCHA_PUBLIC_KEY = environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True

# don't share this with anybody.
SECRET_KEY = 'm$$nd-ugg@5y)_v+8i($)2_ya5z!0rq=tvtplhim#=hml-8-@5'

INSTALLED_APPS = ['otree', 'captcha']

