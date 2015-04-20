from rules import register, Rule
import socket


class TCPRule(Rule):
    
    def filter_condition(self, pywall_packet):
        return pywall_packet.get_protocol() == socket.IPPROTO_TCP

register(TCPRule)
