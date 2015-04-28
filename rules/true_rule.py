"""Rule that is always true."""
from rules import register, SimpleRule


class TrueRule(SimpleRule):
    """Rule that is always true."""

    def filter_condition(self, pckt):
        return True

register(TrueRule)
