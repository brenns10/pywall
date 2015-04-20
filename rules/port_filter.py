import socket


class PortFilter(object):
    """Class for filtering out packets to/from a single port"""
    def __init__(self, **kwargs):  #protocol, match_callback, src_port=None, dst_port=None):
        self._protocol = kwargs.get('protocol', None)
        self._src_port = kwargs.get('src_port', None)
        self._dst_port = kwargs.get('dst_port', None)
        self._action = kwargs.get('action', None)

        if protocol == 'TCP':
            self._protocol = socket.IPPROTO_TCP
        elif protocol == 'UDP':
            self._protocol = socket.IPPROTO_UDP
        else:
            raise ValueError('protocol should be either TCP or UDP')

        if src_port == None and dst_port == None:
            raise ValueError('At least one of src_port or dst_port should be non-None')

    def _is_packet_match(self, packet):
        match = (packet.get_protocol() == self._protocol)
        match = match and (self._src_port == None or packet.get_src_port() == self._src_port)
        match = match and (self._dst_port == None or packet.get_dst_port() == self._dst_port)
        return match

    def __call__(self, packet):
        if self._is_packet_match(packet):
            return self._action
        return False


class PortRangeFilter(object):
    """Blocks all packets with given protocol on inclusive range [lo, hi]."""
    def __init__(self, **kwargs):  #protocol, match_callback, src_range=(None,None), dst_range=(None,None)):
        protocol = kwargs.get('protocol', None)
        self._src_lo = kwargs.get('src_lo', None)
        self._src_hi = kwargs.get('src_hi', None)
        self._dst_lo = kwargs.get('dst_lo', None)
        self._dst_hi = kwargs.get('dst_hi', None)
        self._src_range = (self._src_lo, self._src_hi)
        self._dst_range = (self._dst_lo, self._dst_hi)
        self._action = kwargs.get('action', NONE)

        if protocol == 'TCP':
            self._protocol = socket.IPPROTO_TCP
        elif protocol == 'UDP':
            self._protocol = socket.IPPROTO_UDP
        else:
            raise ValueError('protocol should be either TCP or UDP')

        if self._src_range == (None, None) and self._dst_range == (None, None):
            raise ValueError('At least one of src_port or dst_port should be non-None')
        elif not _is_port_range_valid(self._src_lo, self._src_hi):
            raise ValueError('Invalid source port range')
        elif not _is_port_range_valid(self._dst_lo, self._dst_hi):
            raise ValueError('Invalid destination port range')

    def _is_port_range_valid(self, port_lo, port_hi):
        valid = (port_hi == None and port_lo == None) or (port_hi != None and port_lo != None)
        valid = valid and (port_lo <= port_hi)
        return valid

    def _is_packet_match(self, packet):
        match = (packet.get_protocol() == self._protocol)
        match = match and (self._src_range == (None, None) or
                           (self.src_lo <= packet.get_src_port() <= self._src_hi))
        match = match and (self._dst_range == (None, None) or
                           (self.dst_lo <= packet.get_dst_port() <= self._dst_hi))
        return match

    def __call__(self, packet):
        if self._is_packet_match(packet):
            return self._action
        return False

register(PortFilter)
register(PortRangeFilter)
