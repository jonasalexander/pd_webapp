from otree.api import (
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    models
)
from captcha.fields import ReCaptchaField

doc = """
This application validates that the participant is human.
"""

class Constants(BaseConstants):
    name_in_url = 'validation'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    captcha = models.StringField(blank=True)
    # tbh not sure why I need this
