"""Contains rules that match TCP packets, and track state."""
import socket

from rules import register, SimpleRule
from packets import to_tuple
from pywall import get_pipe


class TCPRule(SimpleRule):
    """Returns True when a packet is TCP."""

    def filter_condition(self, pywall_packet):
        return pywall_packet.get_protocol() == socket.IPPROTO_TCP


class TCPStateRule(TCPRule):
    """A rule that matches TCP packets in a certain state.

    This rule works with the PyWallCracker.  It takes two arguments:
    - match_if: A list of TCP states the rule will match.
    - match_if_not: A list of TCP states the rule will fail to match.

    You cannot provide both arguments.  Only one.  The rule queries the state
    table, and then matches if it is in the the match_if set, or fails if it is
    in the match_if_not.

    """

    def __init__(self, **kwargs):
        """Create rule with arguments."""
        TCPRule.__init__(self, **kwargs)
        self.match_if = set(kwargs.get('match_if', []))
        self.match_if_not = set(kwargs.get('match_if_not', []))
        if self.match_if and self.match_if_not:
            raise ValueError('You may only provide one of "match_if" and'
                             ' "match_if_not".')
        if not self.match_if and not self.match_if_not:
            raise ValueError('You must provide one of "match_if" and'
                             ' "match_if_not".')

    def add_connection(self, pywall_packet):
        """
        Add a connection to the Rule. Connections are represented as the TCP
        4-tuple. See the TCPPacket class for more info.
        """
        self._existing_connections.add(pywall_packet.to_tuple())

    def filter_condition(self, pywall_packet):
        if not TCPRule.filter_condition(self, pywall_packet):
            return False
        pipe = get_pipe()
        pipe.send(to_tuple(pywall_packet))
        state = pipe.recv()
        if self.match_if:
            return state in self.match_if
        else:
            return state not in self.match_if_not


register(TCPRule)
register(TCPStateRule)
