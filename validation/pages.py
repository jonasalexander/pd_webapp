from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from captcha.fields import ReCaptchaField


class Validation(Page):
    __allow_custom_attributes = True
    form_model = 'player'
    form_fields = []

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields['captcha'] = ReCaptchaField()
        return frm

class Summary(Page):
    pass

class Introduction(Page):
    # timeout_seconds = 100 TODO: Do we want this? on summary too? other instructions

    def vars_for_template(self):
        all_stakes=[[k, Constants.payoffs[k]] for k in Constants.payoffs.keys()]
        return dict(all_stakes=all_stakes)


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['compr_q1', 'compr_q2', 'compr_q3', 'compr_q4', 'compr_q5']

    def error_message(self, values):
        if (values['compr_q1'] != Constants.compr_q1_opts[0]
           or values['compr_q2'] != Constants.compr_q2_opts[0]
           or values['compr_q3'] != Constants.compr_q3_opts[0]
           or values['compr_q4'] != Constants.compr_q4_opts[0]
           or values['compr_q5'] != Constants.compr_q5_opts[0]):
            self.player.num_failures += 1
            return "One or more answers incorrect"

    def vars_for_template(self):
        all_stakes=[[k, Constants.payoffs[k]] for k in Constants.payoffs.keys()]
        return dict(all_stakes=all_stakes)


page_sequence = [Validation, Summary, Introduction, ComprehensionCheck]
