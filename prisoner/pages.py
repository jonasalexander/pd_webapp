from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

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
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
            next_stakes=next_stakes,
            current_round=self.round_number
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
