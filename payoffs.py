from otree.api import Currency as c

class Payoffs():
    def __init__(self, betray, betrayed, both_cooperate, both_defect):
        self.betray = c(betray)
        self.betrayed = c(betrayed)
        self.both_cooperate = c(both_cooperate)
        self.both_defect = c(both_defect)

    def __str__(self):
        return f"betray: {self.betray}, betrayed: {self.betrayed}, both_cooperate: {self.both_cooperate}, both_defect: {self.both_defect}"

payoffs = Payoffs(betray=c(0.35), betrayed=c(0.05), both_cooperate=c(0.25), both_defect=c(0.15))