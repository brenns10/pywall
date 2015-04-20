"""Collection of rules for PyWall."""

import os
import glob

rules = {}
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]


class Rule(object):
    """
    One rule class to rule them all.

    Generic Rule class. All other rules should inherit from here, passing
    their **kwargs up to the super constructor. To function as a rule, each
    subclass should provide its own implementation of filter_condition.
    """

    def __init__(self, **kwargs):
        self._action = kwargs.get('action')

    def __call__(self, pywall_packet):
        """
        Packet filtering logic. This is the same for all rules, so this method
        should never be overridden. To get the correct behavior for your rules,
        provide your own implementation of the filter_condition method.
        """
        if self.filter_condition(pywall_packet):
            return self._action
        else:
            return False

    def filter_condition(self, pywall_packet):
        """
        This method determines whether this rule should allow the packet
        through. Override this in subclasses to define correct behavior for
        your rule. This method should return a boolean.
        """
        return True


def register(rule_class):
    rules[rule_class.__name__] = rule_class
