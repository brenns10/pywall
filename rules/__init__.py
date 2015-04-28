"""Collection of rules for PyWall."""

import os
import glob
from abc import ABCMeta
from abc import abstractmethod

rules = {}
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]


class Rule(object):
    """
    One rule class to rule them all.

    Generic Rule class. All other rules should inherit from here, passing
    their **kwargs up to the super constructor. To function as a rule, each
    subclass should provide its own implementation of __call__.

    This class should be extended instead of SimpleRule if multiple actions
    need to be supported.
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self._action = kwargs.get('action')

    @abstractmethod
    def __call__(self, pywall_packet):
        """
        Return False to pass packet down the chain, "ACCEPT" to
        explicitly accept and "DROP" to explicitly drop.
        """
        pass


class SimpleRule(Rule):
    """
    Class for simple rules (i.e. ones that perform one action if some condition
    is met, pass down the chain otherwise).
    """
    __metaclass__ = ABCMeta

    def __call__(self, pywall_packet):
        """
        Packet filtering logic. This is the same for all simple rules, so this
        method should never be overridden. To get the correct behavior for your
        rules, provide your own implementation of the filter_condition method.
        """
        if self.filter_condition(pywall_packet):
            return self._action
        else:
            return False

    @abstractmethod
    def filter_condition(self, pywall_packet):
        """
        Return True to perform default action, return False to pass packet
        down the chain. Override this to define correct behavior for your rule.
        """
        return True


def register(rule_class):
    """This function must be called in every rule class."""
    rules[rule_class.__name__] = rule_class
