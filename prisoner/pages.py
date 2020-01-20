from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from numpy.random import geometric

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


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
