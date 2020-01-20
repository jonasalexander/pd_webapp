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


class Payoffs():
    def __init__(self, betray, betrayed, both_cooperate, both_defect):
        self.betray = c(betray)
        self.betrayed = c(betrayed)
        self.both_cooperate = c(both_cooperate)
        self.both_defect = c(both_defect)


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    base_rounds = 20
    num_rounds = base_rounds+25 #effectively max

    instructions_template = 'prisoner/instructions.html'

    payoffs = {"high": Payoffs(betray=c(300), betrayed=c(0), both_cooperate=c(200), both_defect=c(100)),
               "low": Payoffs(betray=c(30), betrayed=c(0), both_cooperate=c(20), both_defect=c(10))}

    default_stakes = "high"


class Subsession(BaseSubsession):
    stakes = models.StringField(initial=Constants.default_stakes)

    def set_stakes(self):
        if self.round_number == 1:
            pass
        else:
            self.stakes = "high"
            for p in self.get_players():
                if p.in_round(self.round_number - 1).decision == "Defect":
                    self.stakes = "low"


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
        payoff_matrix = dict(
            Cooperate=dict(
                Cooperate=Constants.payoffs[self.subsession.stakes].both_cooperate,
                Defect=Constants.payoffs[self.subsession.stakes].betrayed,
            ),
            Defect=dict(
                Cooperate=Constants.payoffs[self.subsession.stakes].betray, Defect=Constants.payoffs[self.subsession.stakes].both_defect
            ),
        )

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
