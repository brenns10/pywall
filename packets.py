from __future__ import unicode_literals
from struct import unpack
from struct import pack
import socket


def payload_builder(buff, protocol):
    """If `protocol` is supported, builds packet object from buff."""
    return None  # so sue me


class IPPacket(object):
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
        self._options = [buff[(20+i):(20+i+4)] for i in range(0, 4 * (self._ihl - 5), 4)]

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
        return u'IP from %s to %s, id=%d, len=%d, ttl=%d' % (self._src_ip, self._dest_ip, 
                                                             self._id, self._total_length, self._ttl)

    def __len__(self):
        """Returns the total length of the IP message."""
        return self.total_length

