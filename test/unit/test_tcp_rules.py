import unittest
from rules import tcp_rules
from test.unit.fake_packet import FakePacket
import socket


class TestTCPRule(unittest.TestCase):

    def test_udp_packet(self):
        rule = tcp_rules.TCPRule()
        packet = FakePacket(protocol=socket.IPPROTO_UDP)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_packet(self):
        rule = tcp_rules.TCPRule()
        packet = FakePacket(protocol=socket.IPPROTO_TCP)
        self.assertTrue(rule.filter_condition(packet))

if __name__ == '__main__':
    unittest.main()

