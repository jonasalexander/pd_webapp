from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from numpy.random import geometric
from captcha.fields import ReCaptchaField


class PairingWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class Introduction(Page):
    timeout_seconds = 100

    def before_next_page(self):
        if "num_rounds" not in self.session.vars:
            self.session.vars["num_rounds"] = min(geometric(0.5)+Constants.base_rounds-1, Constants.num_rounds)
            # -1 because of geometric vs first success definition

    def vars_for_template(self):
        self.subsession.set_stakes()
        return dict(stakes=self.subsession.stakes,
            payoffs=Constants.payoffs[self.subsession.stakes])


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['compr_q1', 'compr_q2', 'compr_q3']

    def is_displayed(self):
        return self.round_number == 1
        # only display if first round

    def error_message(self, values):
        if (values['compr_q1'] != Constants.compr_q1_opts[0]
           or values['compr_q2'] != Constants.compr_q2_opts[0]
           or values['compr_q3'] != Constants.compr_q3_opts[0]):
            return "One or more answers incorrect"

    def vars_for_template(self):
        return dict(stakes=self.subsession.stakes,
            payoffs=Constants.payoffs[self.subsession.stakes])


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
         return dict(stakes=self.subsession.stakes,
            payoffs=Constants.payoffs[self.subsession.stakes])


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        next_stakes = "high" if "Defect" not in [me.decision, opponent.decision] else "low"
        last_round = self.round_number == self.session.vars["num_rounds"]
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
            next_stakes=next_stakes,
            last_round=last_round
        )
    
    def app_after_this_page(self, upcoming_apps):
        if self.round_number == self.session.vars["num_rounds"]:
            return "survey"


page_sequence = [PairingWaitPage, Introduction, ComprehensionCheck, Decision, ResultsWaitPage, Results]
