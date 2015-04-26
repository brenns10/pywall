import unittest
from rules import ip_rules
from test.unit.fake_packet import FakePacket


class TestSourceIPRule(unittest.TestCase):

    def test_in_range(self):
        rule = ip_rules.SourceIPRule(cidr_range='127.0.0.0/24')
        packet = FakePacket(src_ip='127.0.0.0')
        self.assertTrue(rule.filter_condition(packet))

    def test_out_of_range(self):
        rule = ip_rules.SourceIPRule(cidr_range='127.0.0.0/24')
        packet = FakePacket(src_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_without_cidr_range(self):
        rule = ip_rules.SourceIPRule(cidr_range='127.0.0.0')
        packet1 = FakePacket(src_ip='127.0.0.0')
        packet2 = FakePacket(src_ip='127.0.0.1')
        self.assertTrue(rule.filter_condition(packet1))
        self.assertFalse(rule.filter_condition(packet2))


class TestDestinationIPRule(unittest.TestCase):

    def test_in_range(self):
        rule = ip_rules.DestinationIPRule(cidr_range='127.0.0.0/24')
        packet = FakePacket(dst_ip='127.0.0.0')
        self.assertTrue(rule.filter_condition(packet))

    def test_out_of_range(self):
        rule = ip_rules.DestinationIPRule(cidr_range='127.0.0.0/24')
        packet = FakePacket(dst_ip='128.0.0.0')
        self.assertFalse(rule.filter_condition(packet))

    def test_without_cidr_range(self):
        rule = ip_rules.DestinationIPRule(cidr_range='127.0.0.0')
        packet1 = FakePacket(dst_ip='127.0.0.0')
        packet2 = FakePacket(dst_ip='127.0.0.1')
        self.assertTrue(rule.filter_condition(packet1))
        self.assertFalse(rule.filter_condition(packet2))


if __name__ == '__main__':
    unittest.main()

