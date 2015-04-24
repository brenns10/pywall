from __future__ import unicode_literals
from struct import unpack
from abc import ABCMeta
from abc import abstractmethod
import socket


def payload_builder(payload_buff, protocol):
    """If `protocol` is supported, builds packet object from buff."""
    if protocol == socket.IPPROTO_TCP:
        return TCPPacket(payload_buff)
    elif protocol == socket.IPPROTO_UDP:
        return UDPPacket(payload_buff)
    else:
        return None


def to_tuple(ippacket, flip=False):
    payload = ippacket.get_payload()
    if type(payload) is TCPPacket and not flip:
        tup = (ippacket.get_src_ip(), payload.get_src_port(),  # remote
               ippacket.get_dst_ip(), payload.get_dst_port())  # local
        return tup
    elif type(payload) is TCPPacket and flip:
        tup = (ippacket.get_dst_ip(), payload.get_dst_port(),  # remote
               ippacket.get_src_ip(), payload.get_src_port())  # local
    else:
        tup = None
    return tup


class Packet(object):
    """Base class for all packets"""
    __metaclass__ = ABCMeta

    def __init__(self, buf):
        """Create packet from raw data."""
        self.buf = buf
        self._src_ip = socket.inet_ntoa(buf[12:16])
        self._dst_ip = socket.inet_ntoa(buf[16:20])
        # Internal Header Length, in bytes
        self._ihl = ((unpack('!B', buf[0]) & 0xF0) >> 4) * 4
        self._proto = unpack('!B', buf[9])
        self._payload = payload_builder(buf[self._ihl:], self._proto)

    def get_src_ip(self):
        return self._src_ip

    def get_dst_ip(self):
        return self._dst_ip

    def get_protocol(self):
        return self._proto

    def get_payload(self):
        return self._payload

    @abstractmethod
    def get_header_len(self):
        return self._ihl

    @abstractmethod
    def get_data_len(self):
        return len(self.buf) - self._ihl


class TransportLayerPacket(Packet):
    """Base class packets at the transport layer """
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_body(self):
        pass

# IPPacket class should go here

class TCPPacket(TransportLayerPacket):
    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        self._src_port, self._dst_port = unpack('!HH', buff[0:4])
        self._seq_num, self._ack_num = unpack('!II', buff[4:12])
        flags, self._win_size = unpack('!HH', buff[12:16])
        self._data_offset = flags & 0xF000
        self.flag_ns  = flags & 0x0100
        self.flag_cwr = flags & 0x0080
        self.flag_ece = flags & 0x0040
        self.flag_urg = flags & 0x0020
        self.flag_ack = flags & 0x0010
        self.flag_psh = flags & 0x0008
        self.flag_rst = flags & 0x0004
        self.flag_syn = flags & 0x0002
        self.flag_fin = flags & 0x0001
        self._checksum, self._urg_ptr = unpack('!HH', buff[16:20])
        self._options = buff[20:(self._data_offset * 4)]  # can be parsed later if we care
        self._total_length = len(buff)
        self._body = buff[self.get_header_len():]

    def get_header_len(self):
        return self._data_offset * 4

    def get_data_len(self):
        return self._total_length - self.get_header_len()

    def get_src_port(self):
        return self._src_port
    
    def get_dst_port(self):
        return self._dst_port

    def get_body(self):
        return str(self._body)

    def __unicode__(self):
        """Returns a printable version of the TCP header"""
        return u'TCP from %d to %d' % (self._src_port, self._dst_port)


class UDPPacket(TransportLayerPacket):
    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        self._src_port, self._dst_port = unpack('!HH', buff[0:4])
        self._length, self._checksum = unpack('!HH', buff[4:8])
        self._total_length = len(buff)
        self._body = buff[self.get_header_len():]

    def get_header_len(self):
        return 8

    def get_data_len(self):
        return self._total_length - self.get_header_len()

    def get_src_port(self):
        return self._src_port
    
    def get_dst_port(self):
        return self._dst_port

    def get_body(self):
        return str(self._body)


    def __unicode__(self):
        """Returns a printable version of the UDP header"""
        return u'UDP from %d to %d' % (self._src_port, self._dst_port)
