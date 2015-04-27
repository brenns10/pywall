"""PyWall instance creator from config file."""

from __future__ import print_function
import json

import rules
from rules import *
from pywall import PyWall


class PyWallConfig(object):

    def __init__(self, filename):
        self.filename = filename

    def create_pywall(self, *args):

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
