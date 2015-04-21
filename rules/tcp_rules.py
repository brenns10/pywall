from rules import register, Rule
from packets import to_tuple
from pywall import get_pipe
import socket


class TCPRule(Rule):

    def filter_condition(self, pywall_packet):
        return pywall_packet.get_protocol() == socket.IPPROTO_TCP


class TCPStateRule(TCPRule):

    def __init__(self, **kwargs):
        TCPRule.__init__(self, **kwargs)
        self.match_if = set(kwargs.get('match_if', []))
        self.match_if_not = set(kwargs.get('match_if_not', []))

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
        print('request state')
        pipe.send(to_tuple(pywall_packet))
        state = pipe.recv()
        print('receive state %s' % state)
        return state in self.match_if and state not in self.match_if_not


register(TCPRule)
register(TCPStateRule)
