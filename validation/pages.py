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
    def vars_for_template(self):
        return dict(max_bonus=Constants.max_bonus, min_bonus=Constants.min_bonus, participation_fee=self.session.config['participation_fee'])

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def vars_for_template(self):
        return dict(max_bonus=Constants.max_bonus, min_bonus=Constants.min_bonus, participation_fee=self.session.config['participation_fee'])

class Introduction(Page):

    def vars_for_template(self):
        rand_ex = (randint(0, 1), randint(0, 1))
        self.player.validation_rand_ex = dumps(rand_ex)
        ex_stakes=[Constants.default_stakes, Constants.payoffs[Constants.default_stakes]]
        all_stakes=[[k, Constants.payoffs[k]] for k in Constants.payoffs.keys()]
        return dict(all_stakes=all_stakes, rand_ex=rand_ex, ex_stakes=ex_stakes)


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['compr_q1', 'compr_q2', 'compr_q3', 'compr_q4', 'compr_q5', 'compr_q6']

    def error_message(self, values):
        if (values['compr_q1'] != Constants.compr_q1_opts[0]
           or values['compr_q2'] != Constants.compr_q2_opts[0]
           or values['compr_q3'] != Constants.compr_q3_opts[0]
           or values['compr_q4'] != Constants.compr_q4_opts[0]
           or values['compr_q5'] != Constants.compr_q5_opts[0]
           or values['compr_q6'] != Constants.compr_q6_opts[0]):
            self.player.num_failures += 1
            return "One or more answers incorrect"

    def vars_for_template(self):
        rand_ex = loads(self.player.validation_rand_ex)
        ex_stakes=[Constants.default_stakes, Constants.payoffs[Constants.default_stakes]]
        all_stakes=[[k, Constants.payoffs[k]] for k in Constants.payoffs.keys()]
        return dict(all_stakes=all_stakes, rand_ex=rand_ex, ex_stakes=ex_stakes)

page_sequence = [Validation, Consent, Welcome, Introduction, ComprehensionCheck]
