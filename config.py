"""PyWall instance creator from config file."""

from __future__ import print_function
import json

import rules
# This import must be here to trigger all rules to be imported and register.
from rules import *
from pywall import PyWall


class PyWallConfig(object):
    """Creates instances of PyWall from a configuration file."""

    def __init__(self, filename):
        """Constructor - takes filename, but doesn't open."""
        self.filename = filename

    def create_pywall(self, *args):
        """Read the configuration file and create an instance of PyWall.

        Any arguments will be passed to the constructor of PyWall.

        """
        cfg = json.load(open(self.filename))
        default = cfg.pop('default_chain', 'ACCEPT')

        the_wall = PyWall(*args, default=default)

        for chain, rule_list in cfg.items():
            the_wall.add_chain(chain)

            for rule in rule_list:
                name = rule.pop('name', None)
                rule_class = rules.rules[name]
                rule_instance = rule_class(**rule)
                the_wall.add_brick(chain, rule_instance)

        return the_wall
