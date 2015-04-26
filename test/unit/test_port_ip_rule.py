import unittest
from rules.port_ip_rule import AddressPortRule
from test.unit.fake_packet import FakePacket
import socket


class TestAddressPortRule(unittest.TestCase):

    def test_port_rule_only_match(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_port_rule_only_mismatch(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_src_rule_both_match(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='127.0.0.0')
        self.assertTrue(rule.filter_condition(packet))

    def test_port_and_src_rule_port_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, src_ip='127.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_src_rule_src_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_src_rule_both_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, src_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_dst_rule_both_match(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_ip='127.0.0.0')
        self.assertTrue(rule.filter_condition(packet))

    def test_port_and_dst_rule_port_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, dst_ip='127.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_dst_rule_dst_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_and_dst_rule_both_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_all_match(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='127.0.0.0', dst_ip='127.0.0.0')
        self.assertTrue(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_port_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, src_ip='127.0.0.0', dst_ip='127.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_src_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='128.0.0.0', dst_ip='127.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_dst_fails(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='127.0.0.0', dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_port_and_src_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, src_ip='128.0.0.0', dst_ip='127.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_port_and_dst_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, src_ip='127.0.0.0', dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_src_and_dst_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, src_ip='128.0.0.0', dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_port_src_and_dst_rule_all_fail(self):
        rule = AddressPortRule(protocol='UDP', src_lo=0, src_hi=1, src_ip='127.0.0.0/24', dst_ip='127.0.0.0/24')
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, src_ip='128.0.0.0', dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))


if __name__ == '__main__':
    unittest.main()

