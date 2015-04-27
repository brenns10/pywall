import unittest
import socket
from rules import port_filter
from test.unit.fake_packet import FakePacket


class TestPortRule(unittest.TestCase):

    def test_udp_filter_with_tcp_packet(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_with_udp_matching_src_port(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_upd_filter_udp_packet_wrong_src_port(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_matching_dst_port(self):
        rule = port_filter.PortRule(protocol='UDP', dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_wrong_dst_port(self):
        rule = port_filter.PortRule(protocol='UDP', dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_matching_src_and_dst(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_right_src_wrong_dst(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_wrong_src_right_dst(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=1, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_wrong_src_wrong_dst(self):
        rule = port_filter.PortRule(protocol='UDP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=1, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_udp_packet(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_UDP)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_matching_src_port(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcd_filter_tcp_packet_wrong_src_port(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_matching_dst_port(self):
        rule = port_filter.PortRule(protocol='TCP', dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_wrong_dst_port(self):
        rule = port_filter.PortRule(protocol='TCP', dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_matching_src_and_dst(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_right_src_wrong_dst(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_wrong_src_right_dst(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=1, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_wrong_src_wrong_dst(self):
        rule = port_filter.PortRule(protocol='TCP', src_port=0, dst_port=0)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=1, dst_port=1)
        self.assertFalse(rule.filter_condition(packet))

class TestPortRangeFilter(unittest.TestCase):

    def test_udp_filter_tcp_packet(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_in_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_out_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_in_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_out_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_in_src_range_and_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_in_src_range_not_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=0, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_in_dst_range_not_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, dst_port=0)
        self.assertFalse(rule.filter_condition(packet))

    def test_udp_filter_udp_packet_not_in_src_range_or_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='UDP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP, src_port=5, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_udp_packet(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_UDP)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_in_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_out_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_in_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_out_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_in_src_range_and_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, dst_port=0)
        self.assertTrue(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_in_src_range_not_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=0, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_in_dst_range_not_src_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=5, dst_port=0)
        self.assertFalse(rule.filter_condition(packet))

    def test_tcp_filter_tcp_packet_not_in_src_range_or_dst_range(self):
        rule = port_filter.PortRangeFilter(protocol='TCP', src_lo=0, src_hi=1, dst_lo=0, dst_hi=1)
        packet = FakePacket(protocol=socket.IPPROTO_TCP, src_port=5, dst_port=5)
        self.assertFalse(rule.filter_condition(packet))
   

if __name__ == '__main__':
    unittest.main()

