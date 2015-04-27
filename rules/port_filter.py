"""Contains rules for filtering by TCP/UDP port."""

import socket

from rules import register
from rules import SimpleRule


class PortRule(SimpleRule):
    """Class for filtering out packets to/from a single port"""

    def __init__(self, **kwargs):
        """Create a rule for a single source and/or destination port."""
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

        if self._src_port is None and self._dst_port is None:
            raise ValueError('At least one of src_port or dst_port should be'
                             ' non-None')

    def filter_condition(self, packet):
        """Condition to jump to action chain."""
        match = (packet.get_protocol() == self._protocol)
        match = match and (self._src_port is None or
                           packet.get_payload().get_src_port() == self._src_port)
        match = match and (self._dst_port is None or
                           packet.get_payload().get_dst_port() == self._dst_port)
        if match:
            print('PortRule: %s' % str(self._action))
        return match


class PortRangeRule(SimpleRule):
    """Blocks all packets with given protocol on inclusive range [lo, hi]."""

    def __init__(self, **kwargs):
        """Creates a rule that takes matches port ranges."""
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
            raise ValueError('At least one of src_port or dst_port should be'
                             ' non-None')
        elif not self._is_port_range_valid(self._src_lo, self._src_hi):
            raise ValueError('Invalid source port range')
        elif not self._is_port_range_valid(self._dst_lo, self._dst_hi):
            raise ValueError('Invalid destination port range')

    def _is_port_range_valid(self, port_lo, port_hi):
        """Return true if a port range is valid."""
        valid = (port_hi is None and port_lo is None) or \
                (port_hi is not None and port_lo is not None)
        valid = valid and (port_lo <= port_hi)
        return valid

    def filter_condition(self, packet):
        """Condition to jump to action chain."""
        src_port = packet.get_payload().get_src_port()
        dst_port = packet.get_payload().get_dst_port()
        match = (packet.get_protocol() == self._protocol)
        match = match and ((self._src_range == (None, None)) or
                           (self._src_lo <= src_port <= self._src_hi))
        match = match and ((self._dst_range == (None, None)) or
                           (self._dst_lo <= dst_port <= self._dst_hi))
        if match:
            print('PortRangeRule: %s' % str(self._action))
        return match


register(PortRule)
register(PortRangeRule)
