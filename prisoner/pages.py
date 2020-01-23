from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from numpy.random import geometric
from captcha.fields import ReCaptchaField


class PairingWaitPage(WaitPage):
    title_text = "Please Wait"
    body_text = "You're all set to complete the HIT! Waiting to pair you with the next available participant..."

    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def before_next_page(self):
        if "num_rounds" not in self.session.vars:
            self.session.vars["num_rounds"] = min(geometric(0.5)+Constants.base_rounds-1, Constants.num_rounds)
            # -1 because of geometric vs first success definition

    def vars_for_template(self):
        self.subsession.set_stakes()
        return dict(stakes=self.subsession.stakes,
            payoffs=Constants.payoffs[self.subsession.stakes])


class ResultsWaitPage(WaitPage):
    title_text = "Please Wait"
    body_text = "Waiting for the other participant to finish..."


    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()

        next_stakes = "high" if "Defect" not in [me.decision, opponent.decision] else "low"

        last_round = self.round_number == self.session.vars["num_rounds"]

        last_digit = self.session.vars["num_rounds"] % 10
        if last_digit == 1:
            round_str = str(self.session.vars["num_rounds"])+"st"
        elif last_digit == 2:
            round_str = str(self.session.vars["num_rounds"])+"nd"
        elif last_digit == 3:
            round_str = str(self.session.vars["num_rounds"])+"rd"
        else:
            round_str = str(self.session.vars["num_rounds"])+"th"

        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
            next_stakes=next_stakes,
            last_round=last_round,
            num_rounds=self.session.vars["num_rounds"],
            round_str=round_str
        )
    
    def app_after_this_page(self, upcoming_apps):
        if self.round_number == self.session.vars["num_rounds"]:
            return "survey"

page_sequence = [PairingWaitPage, Decision, ResultsWaitPage, Results]
