"""Contains rules for filtering by IP address."""
import netaddr

from rules import register, SimpleRule


class IPRangeRule(SimpleRule):
    """Filter IP packets based on source/dest address."""

    def __init__(self, **kwargs):
        """Create an IPRangeRule, taking the cidr_range."""
        SimpleRule.__init__(self, **kwargs)
        self._ip_range = netaddr.IPNetwork(kwargs['cidr_range'])


class SourceIPRule(IPRangeRule):
    """Filter IP packets based on source address"""

    def __init__(self, **kwargs):
        """Takes single argument, 'cidr_range', passed to super."""
        IPRangeRule.__init__(self, **kwargs)

    def filter_condition(self, pywall_packet):
        """
        Filter packets if their source address falls within the ip_range.
        """
        return pywall_packet.get_src_ip() in self._ip_range


class DestinationIPRule(IPRangeRule):
    """Filter IP packets based on destination address"""

    def __init__(self, **kwargs):
        """Takes single argument, 'cidr_range', passed to super."""
        IPRangeRule.__init__(self, **kwargs)

    def filter_condition(self, pywall_packet):
        """True if destination address falls within the ip_range."""
        return pywall_packet.get_dst_ip() in self._ip_range

register(SourceIPRule)
register(DestinationIPRule)
