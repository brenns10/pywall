from rules import register, Rule
import socket


class TCPRule(Rule):
    
    def filter_condition(self, pywall_packet):
        return pywall_packet.get_protocol() == socket.IPPROTO_TCP


class TCPExistingConnectionRule(TCPRule):

    def __init__(self, **kwargs):
        TCPRule.__init__(self, **kwargs)
        self._existing_connections = set()

    def add_connection(self, pywall_packet):
        """
        Add a connection to the Rule. Connections are represented as the TCP
        4-tuple. See the TCPPacket class for more info.
        """
        self._existing_connections.add(pywall_packet.to_tuple())

    def filter_condition(self, pywall_packet):
        return TCPRule.filter_condition(pywall_packet) and \
                pywall_packet.to_tuple() in self._existing_connections

register(TCPRule)
register(TCPExistingConnectionRule)
