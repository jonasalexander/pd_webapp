from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

doc = """
This is a repeated "Prisoner's Dilemma" with varying stakes. Two players are 
asked separately whether they want to cooperate or defect. Their choices 
directly determine the payoffs as well as the stakes for the next round.
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    num_rounds = 3

    instructions_template = 'prisoner/instructions.html'

    # high stakes payoff if 1 player defects and the other cooperates""",
    high_betray_payoff = c(300)
    high_betrayed_payoff = c(0)

    # high stakes payoff if both players cooperate or both defect
    high_both_cooperate_payoff = c(200)
    high_both_defect_payoff = c(100)

    # low stakes payoff if 1 player defects and the other cooperates""",
    low_betray_payoff = c(30)
    low_betrayed_payoff = c(0)

    # low stakes payoff if both players cooperate or both defect
    low_both_cooperate_payoff = c(20)
    low_both_defect_payoff = c(10)
    
    default_stakes_high = True


class Subsession(BaseSubsession):
    stakes_high = models.BooleanField(initial=Constants.default_stakes_high)

    def set_stakes(self):
        if self.round_number == 1:
            pass
        else:
            self.stakes_high = 1
            for p in self.get_players():
                if p.in_round(self.round_number - 1).decision == "Defect":
                    self.stakes_high = 0


class Group(BaseGroup):

    def set_payoffs(self):

        for p in self.get_players():
            p.set_payoff()

class Player(BasePlayer):
    decision = models.StringField(
        choices=[['Cooperate', 'Cooperate'], ['Defect', 'Defect']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        if self.subsession.stakes_high:
            payoff_matrix = dict(
                Cooperate=dict(
                    Cooperate=Constants.high_both_cooperate_payoff,
                    Defect=Constants.high_betrayed_payoff,
                ),
                Defect=dict(
                    Cooperate=Constants.high_betray_payoff, Defect=Constants.high_both_defect_payoff
                ),
            )
        else:
            payoff_matrix = dict(
                Cooperate=dict(
                    Cooperate=Constants.low_both_cooperate_payoff,
                    Defect=Constants.low_betrayed_payoff,
                ),
                Defect=dict(
                    Cooperate=Constants.low_betray_payoff, Defect=Constants.low_both_defect_payoff
                ),
            )

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
