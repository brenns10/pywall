from __future__ import unicode_literals
from struct import unpack
from struct import pack
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


class Packet(object):
    """Base class for all packets"""
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_header_len(self):
        pass

    @abstractmethod
    def get_data_len(self):
        pass


class TransportLayerPacket(Packet):
    """Base class packets at the transport layer """
    __metaclass__ = ABCMeta


class IPPacket(Packet):
    """
    Builds a packet object from a raw IP datagram stream.

    If possible, also builds the packet object of the payload.
    Reference: http://www.binarytides.com/raw-socket-programming-in-python-linux/

    The original version of class was also used in Jeff's EECS 325 project 2.
    Might be worth checking with Podgurski before continuing.
    """
    def __init__(self, buff):
        self._parse_header(buff)
        self._payload = payload_builder(buff[self.get_header_len():], self._protocol)

    def _parse_header(self, buff):
        v_ihl, dscp_ecn, self._total_length = unpack('!BBH', buff[0:4])
        self._version = (v_ihl >> 4) & 0xF
        self._ihl = v_ihl & 0xF
        self._dscp = (dscp_ecn >> 3) & 0x1F
        self._ecn = dscp_ecn & 0x7
        self._id, flag_frag = unpack('!HH', buff[4:8])
        self._flags = (flag_frag >> 13) & 0x7
        self._frag_offset = flag_frag & 0x1FFF
        self._ttl, self._protocol, self._checksum = unpack('!BBH', buff[8:12])
        self._src_ip = socket.inet_ntoa(buff[12:16])
        self._dest_ip = socket.inet_ntoa(buff[16:20])
        self._options = buff[20:(self._ihl * 4)]  # can be parsed later if we care

    def get_header_len(self):
        return self._ihl * 4

    def get_data_len(self):
        return self._total_length - self._ihl * 4

    def get_protocol(self):
        return self._protocol

    def get_payload(self):
        return self._payload

    def __unicode__(self):
        """Returns a printable 'string' representation of the IPHeader"""
        return u'IP from %s to %s, id=%d, pload_t=%s' % (self._src_ip, self._dest_ip,
                                                           self._id, self._payload)

class TCPPacket(TransportLayerPacket):
    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        self._src_port, self._dest_port = unpack('!HH', buff[0:4])
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

    def get_header_len(self):
        return self._data_offset * 4

    def get_data_len(self):
        return self._total_length - self.get_header_len()

    def get_src_port(self):
        return self._src_port
    
    def get_dst_port(self):
        return self._dst_port

    def __unicode__(self):
        """Returns a printable version of the TCP header"""
        return u'TCP from %d to %d' % (self._src_port, self._dest_port)


class UDPPacket(TransportLayerPacket):
    def __init__(self, buff):
        self._parse_header(buff)

    def _parse_header(self, buff):
        self._src_port, self._dest_port = unpack('!HH', buff[0:4])
        self._length, self._checksum = unpack('!HH', buff[4:8])
        self._total_length = len(buff)

    def get_header_len(self):
        return 8

    def get_data_len(self):
        return self._total_length - self.get_header_len()

    def get_src_port(self):
        return self._src_port
    
    def get_dst_port(self):
        return self._dst_port

    def __unicode__(self):
        """Returns a printable version of the UDP header"""
        return u'UDP from %d to %d' % (self._src_port, self._dest_port)
