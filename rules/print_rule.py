"""Printout rule for PyWall."""

from __future__ import print_function
from rules import register
import logging


class PrintRule(object):

    def __call__(self, packet):
        """Prints out packet information at the IP level."""
        logging.debug(unicode(packet))
        logging.debug(unicode(packet.get_payload()))
        return False


register(PrintRule)
