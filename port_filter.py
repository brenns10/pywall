import socket


class PortFilter(object):
    """Class for filtering out packets to/from a single port"""
    def __init__(self, protocol, match_callback, src_port=None, dst_port=None):
        self._protocol = protocol
        self._src_port = src_port
        self._dst_port = dst_port
        self._match_callback = match_callback

        if protocol != socket.IPPROTO_TCP and protocol != socket.IPPROTO_UDP:
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
            return self._match_callback()
        return False


class PortRangeFilter(object):
    def __init__(self, protocol, match_callback, src_range=(None,None), dst_range=(None,None)):
        self._protocol = protocol
        self._src_range = src_range
        self._dst_range = dst_range
        self._src_lo, self._src_hi = src_range
        self._dst_lo, self._dst_hi = dst_range
        self._match_callback = match_callback

        if protocol != socket.IPPROTO_TCP and protocol != socket.IPPROTO_UDP:
            raise ValueError('protocol should be either TCP or UDP')
        if src_range == (None, None) and dst_range == (None, None):
            raise ValueError('At least one of src_port or dst_port should be non-None')
        elif not _is_port_range_valid(src_range) or not _is_port_range_valid(dst_range):
            raise ValueError('Invalid port range(s)')

    def _is_port_range_valid(self, port_range):
        port_lo, port_hi = port_range
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
            return self._match_callback()
        return False
