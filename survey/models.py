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


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    gender_options = ['Male', 'Female', 'Non-binary/third gender', 'Other', 'Prefer not to answer']
    income_options = ['$0-10,000', '$10,001-30,000', '$30,001-50,000', '$50,001-80,000', 
        '$80,001-120,000', '$120,001 and above']
    ethnicity_options = ['Native American Indian or Alaska Native', 'Asian', 'Black of African American', 
        'Native Hawaiian or Other Pacific Islander', 'White', 'Unknown', 'Do not wish to answer']
    education_options = ['No formal education', 'High school diploma', 'College degree', 'Vocational training',
        'Bachelor\'s degree', 'Master\'s degree', 'Professional degree', 'Doctorate degree', 'Other']
    pd_familiarity_options = ['I had never heard of it', 'That phrase seems familiar, but I didn\'t really know what it is',
        'I knew what it is in theory', 'I had played it before, but rarely (<5)', 'I had played it before, a few times (5-10)',
        'I had played it before, many times (11+)']
 

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.IntegerField(label='What is your age?', min=13, max=125)

    gender = models.StringField(
        choices=[[a]*2 for a in Constants.gender_options],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )

    income = models.StringField(
        choices=[[a]*2 for a in Constants.income_options],
        label='What is your household income?',
        widget=widgets.RadioSelect
    )

    ethnicity = models.StringField(
        choices=[[a]*2 for a in Constants.ethnicity_options],
        label='What is your ethnicity?',
        widget=widgets.RadioSelect
    )

    education = models.StringField(
        choices=[[a]*2 for a in Constants.education_options],
        label='What is your highest level of education?',
        widget=widgets.RadioSelect
    )

    pd_familiarity = models.StringField(
        choices=[[a]*2 for a in Constants.pd_familiarity_options],
        label='How familiar were you with Prisoner\'s Dilemma games before this experiment?',
        widget=widgets.RadioSelect
    )

    feedback = models.TextField(
        label='''This is your chance to submit feedback to us.
        Was there anything you found confusing?''',
        blank=True
    )

    """
    crt_bat = models.IntegerField(
        label='''
        A bat and a ball cost 22 dollars in total.
        The bat costs 20 dollars more than the ball.
        How many dollars does the ball cost?'''
    )

    crt_widget = models.IntegerField(
        label='''
        "If it takes 5 machines 5 minutes to make 5 widgets,
        how many minutes would it take 100 machines to make 100 widgets?"
        '''
    )

    crt_lake = models.IntegerField(
        label='''
        In a lake, there is a patch of lily pads.
        Every day, the patch doubles in size.
        If it takes 48 days for the patch to cover the entire lake,
        how many days would it take for the patch to cover half of the lake?
        '''
    )
    """
