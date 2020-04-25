from otree.api import Currency as c

class Payoffs():
    def __init__(self, betray, betrayed, both_cooperate, both_defect):
        self.betray = c(betray)
        self.betrayed = c(betrayed)
        self.both_cooperate = c(both_cooperate)
        self.both_defect = c(both_defect)

payoffs = {"high": Payoffs(betray=c(0.20), betrayed=c(0.00), both_cooperate=c(0.12), both_defect=c(0.04)),
            "low": Payoffs(betray=c(0.05), betrayed=c(0.00), both_cooperate=c(0.03), both_defect=c(0.01))}

default_stakes = "high"
