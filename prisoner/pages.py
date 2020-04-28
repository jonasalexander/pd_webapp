from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from captcha.fields import ReCaptchaField


class LimitedTimePage(Page):
    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened and not self.session.vars['timed_out']:
            self.session.vars['timed_out'] = self.participant.id
            for m in self.player.in_rounds(1, self.round_number):
                m.payoff = 0


class PairingWaitPage(WaitPage):
    template_name = 'prisoner/PairingWaitPage.html'

    group_by_arrival_time = True

    def vars_for_template(self):
        return dict(title_text="Please Wait", body_text="You're all set to complete the HIT! Waiting to pair you with the next available participant...", participant_code=self.participant.code+"WPTO")

    def is_displayed(self):
        return self.round_number == 1

    after_all_players_arrive = 'set_vars'


class Decision(LimitedTimePage):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return dict(payoffs=Constants.payoffs)


class ResultsWaitPage(WaitPage):
    title_text = "Please Wait"
    body_text = "Waiting for the other participant to finish..."

    after_all_players_arrive = 'set_payoffs'


class Results(LimitedTimePage):

    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()

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
            last_round=last_round,
            num_rounds=self.session.vars["num_rounds"],
            round_str=round_str,
            group_timed_out=self.session.vars['timed_out'],
            self_timed_out=(self.participant.id == self.session.vars['timed_out'])
        )
    
    def app_after_this_page(self, upcoming_apps):
        if (self.round_number == self.session.vars["num_rounds"]
            or self.session.vars['timed_out']):
            return "survey"

page_sequence = [PairingWaitPage, Decision, ResultsWaitPage, Results]
