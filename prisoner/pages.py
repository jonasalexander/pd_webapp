from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

    def vars_for_template(self):
        self.subsession.set_stakes()
        return dict(stakes_high=self.subsession.stakes_high)


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return dict(stakes_high=self.subsession.stakes_high)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        next_stakes_high = "Defect" not in [me.decision, opponent.decision]
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
            next_stakes_high=next_stakes_high,
            current_round=self.round_number
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
