from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'income', 'education', 'pd_familiarity', 'english_first_language', 'feedback']

    def vars_for_template(self):
        return(dict(timed_out=(self.session.vars['timed_out']==self.participant.id)))

class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


page_sequence = [Demographics]
