from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from captcha.fields import ReCaptchaField
from random import randint
from json import loads, dumps

class Validation(Page):
    __allow_custom_attributes = True
    form_model = 'player'
    form_fields = []

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields['captcha'] = ReCaptchaField()
        return frm

class Welcome(Page):
    pass

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

class Introduction(Page):
    # timeout_seconds = 100 TODO: Do we want this? on summary too? other instructions

    def vars_for_template(self):
        rand_ex = (randint(0, 1), randint(0, 1))
        self.player.validation_rand_ex = dumps(rand_ex)
        stakes=Constants.payoffs
        return dict(all_stakes=stakes, rand_ex=rand_ex, ex_stakes=stakes)


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['compr_q2', 'compr_q3', 'compr_q6']

    def error_message(self, values):
        if (values['compr_q2'] != Constants.compr_q2_opts[0]
            or values['compr_q3'] != Constants.compr_q3_opts[0]
            or values['compr_q6'] != Constants.compr_q6_opts[0]):
            self.player.num_failures += 1
            return "One or more answers incorrect"

    def vars_for_template(self):
        rand_ex = loads(self.player.validation_rand_ex)
        stakes=Constants.payoffs
        return dict(all_stakes=stakes, rand_ex=rand_ex, ex_stakes=stakes)

page_sequence = [Validation, Consent, Welcome, Introduction, ComprehensionCheck]
