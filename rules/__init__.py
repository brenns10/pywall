"""Collection of rules for PyWall."""

import os
import glob

rules = {}
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]


def register(rule_class):
    rules[rule_class.__name__] = rule_class
