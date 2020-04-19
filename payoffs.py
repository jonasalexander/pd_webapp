from otree.api import Currency as c

class Payoffs():
    def __init__(self, betray, betrayed, both_cooperate, both_defect):
        self.betray = c(betray)
        self.betrayed = c(betrayed)
        self.both_cooperate = c(both_cooperate)
        self.both_defect = c(both_defect)

payoffs = Payoffs(betray=c(300), betrayed=c(0), both_cooperate=c(200), both_defect=c(100))
