from rules import register
from rules import Rule

import socket

class PortFilter(Rule):
    """Class for filtering out packets to/from a single port"""
    def __init__(self, **kwargs):  #protocol, match_callback, src_port=None, dst_port=None):
        protocol = kwargs.get('protocol', None)
        self._src_port = kwargs.get('src_port', None)
        self._dst_port = kwargs.get('dst_port', None)
        self._action = kwargs.get('action', 'DROP')

        if protocol == 'TCP':
            self._protocol = socket.IPPROTO_TCP
        elif protocol == 'UDP':
            self._protocol = socket.IPPROTO_UDP
        else:
            raise ValueError('protocol should be either TCP or UDP')

        if self._src_port == None and self._dst_port == None:
            raise ValueError('At least one of src_port or dst_port should be non-None')

    def filter_condition(self, packet):
        match = (packet.get_protocol() == self._protocol)
        match = match and (self._src_port == None or packet.get_payload().get_src_port() == self._src_port)
        match = match and (self._dst_port == None or packet.get_payload().get_dst_port() == self._dst_port)
        if match:
            print('PortFilter: %s' % str(self._action))
        return match


class PortRangeFilter(Rule):
    """Blocks all packets with given protocol on inclusive range [lo, hi]."""
    def __init__(self, **kwargs):  #protocol, match_callback, src_range=(None,None), dst_range=(None,None)):
        protocol = kwargs.get('protocol', None)
        self._src_lo = kwargs.get('src_lo', None)
        self._src_hi = kwargs.get('src_hi', None)
        self._dst_lo = kwargs.get('dst_lo', None)
        self._dst_hi = kwargs.get('dst_hi', None)
        self._src_range = (self._src_lo, self._src_hi)
        self._dst_range = (self._dst_lo, self._dst_hi)
        self._action = kwargs.get('action', 'DROP')

        if protocol == 'TCP':
            self._protocol = socket.IPPROTO_TCP
        elif protocol == 'UDP':
            self._protocol = socket.IPPROTO_UDP
        else:
            raise ValueError('protocol should be either TCP or UDP')

        if self._src_range == (None, None) and self._dst_range == (None, None):
            raise ValueError('At least one of src_port or dst_port should be non-None')
        elif not self._is_port_range_valid(self._src_lo, self._src_hi):
            raise ValueError('Invalid source port range')
        elif not self._is_port_range_valid(self._dst_lo, self._dst_hi):
            raise ValueError('Invalid destination port range')

    def _is_port_range_valid(self, port_lo, port_hi):
        valid = (port_hi == None and port_lo == None) or (port_hi != None and port_lo != None)
        valid = valid and (port_lo <= port_hi)
        return valid

    def filter_condition(self, packet):
        src_port = packet.get_payload().get_src_port()
        dst_port = packet.get_payload().get_dst_port()
        match = (packet.get_protocol() == self._protocol)
        match = match and ((self._src_range == (None, None)) or
                           (self._src_lo <= src_port <= self._src_hi))
        match = match and ((self._dst_range == (None, None)) or
                           (self._dst_lo <= dst_port <= self._dst_hi))
        if match:
            print('PortRangeFilter: %s' % str(self._action))
        return match


register(PortFilter)
register(PortRangeFilter)
