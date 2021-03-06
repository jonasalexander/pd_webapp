from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from random import sample
import sys
sys.path.insert(1, '../')
import payoffs as p

doc = """
This application is presented before starting the experiment
or pairing participants and validates that the participant is human.
The app also presents the instructions and presents the subject
with a comprehension check to ensure that they understood them.
"""

class Constants(BaseConstants):
    name_in_url = 'validation'
    players_per_group = None
    num_rounds = 1

    payoffs_template = 'validation/payoffs.html'
    instructions_template = 'validation/instructions.html'

    default_stakes = p.default_stakes

    payoffs = p.payoffs
    max_bonus = 25*payoffs["high"].both_cooperate
    min_bonus = 20*payoffs["low"].betrayed

    compr_q1_opts = ['High and low stakes', 'Multi- and single-player', 'Simple and complicated', 'Short and long']

    compr_q2_opts = ['50%', '0%', '100%']
    compr_q3_opts = ['50%', '0%', '100%']

    compr_q4_opts = ['The next round is the low, not high stakes version', 'I lose, the game is over', 
        'The next round is the single, not multi-player version', 'The next round is the long, not short version',
        'The next round is the high, not low stakes version']

    compr_q5_opts = ['If I and the other worker both choose to cooperate', 'Wait 3 rounds and it happens automatically',
    'Trick question, there are no low and high stakes versions']

    p1 = payoffs["high"]
    compr_q6_opts = ['I get {0}, the other worker gets {0}'.format(p1.both_cooperate),
    'I get {0}, the other worker gets {1}'.format(p1.betray, p1.betrayed),
    'I get {0}, the other worker gets {1}'.format(p1.betray, p1.both_cooperate),
    'I get {0}, the other worker gets {0}'.format(p1.both_defect)]

class Subsession(BaseSubsession):
    if isinstance(Constants.payoffs, dict):
        payoffs = models.StringField(initial=str([(k, str(v)) for k, v in Constants.payoffs.items()]))
    else:
        payoffs = models.StringField(initial=str(Constants.payoffs))

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    captcha = models.StringField(blank=True) # tbh not sure why I need this
    num_failures = models.IntegerField(initial=0)
    validation_rand_ex = models.StringField(blank=True)

    consent = models.BooleanField(
        blank=False,
        widget=widgets.CheckboxInput,
        label="""By marking this checkbox, 
            I agree that I have read the description of this study,
            my questions have been answered via email,
            and I give my consent to participate"""
    )

    compr_q1 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q1_opts, len(Constants.compr_q1_opts))],
        label='What are the two types of games you will play?',
        widget=widgets.RadioSelect
    )

    compr_q2 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q2_opts, len(Constants.compr_q2_opts))],
        label='What is the chance that there will be another round after the 20th round?',
        widget=widgets.RadioSelect
    )

    compr_q3 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q3_opts, len(Constants.compr_q3_opts))],
        label='What is the chance that there will be another round after the 21st round?',
        widget=widgets.RadioSelect
    )

    compr_q4 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q4_opts, len(Constants.compr_q4_opts))],
        label='What happens if you or the other worker chooses to defect?',
        widget=widgets.RadioSelect
    )

    compr_q5 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q5_opts, len(Constants.compr_q5_opts))],
        label='How do you get from the low stakes game back into the high stakes version?',
        widget=widgets.RadioSelect
    )

    compr_q6 = models.StringField(
        choices=[[a]*2 for a in sample(Constants.compr_q6_opts, len(Constants.compr_q6_opts))],
        label='If you and the other worker are playing the high stakes version and both choose to cooperate, what are your rewards?',
        widget=widgets.RadioSelect
    )
