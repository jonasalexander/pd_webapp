from otree.api import Currency as c

class Payoffs():
    def __init__(self, betray, betrayed, both_cooperate, both_defect):
        self.betray = c(betray)
        self.betrayed = c(betrayed)
        self.both_cooperate = c(both_cooperate)
        self.both_defect = c(both_defect)

payoffs = {"high": Payoffs(betray=c(20), betrayed=c(0), both_cooperate=c(12), both_defect=c(4)),
            "low": Payoffs(betray=c(5), betrayed=c(0), both_cooperate=c(3), both_defect=c(1))}

default_stakes = "high"
