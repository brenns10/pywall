from rules import register, SimpleRule

class TrueRule(SimpleRule):

    def filter_condition(self, pckt):
        return True

register(TrueRule)
