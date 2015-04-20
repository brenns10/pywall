"""Printout rule for PyWall."""

from __future__ import print_function
from rules import register, Rule


class PrintRule(Rule):

    def filter_condition(self, pywall_packet):
        """Prints out packet information at the IP level."""
        print(unicode(pywall_packet))
        print(unicode(pywall_packet.get_payload()))
        # Action should not be applied. Ever.
        return False


register(PrintRule)
