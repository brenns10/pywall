"""Printout rule for PyWall."""

from __future__ import print_function
from rules import register


class PrintRule(object):

    def __call__(self, packet):
        """Prints out packet information at the IP level."""
        print(unicode(ip_packet))
        print(unicode(ip_packet.get_payload()))
        return False


register(PrintRule)
