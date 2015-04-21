from rules import register, Rule

class TrueRule(Rule):

    def filter_condition(self, pckt):
        return True

register(TrueRule)
