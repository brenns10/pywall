import netaddr

class IPRule():
    """Filter IP packets based on some filtering condition."""
    def __init__(self, **kwargs):
        """
        action: 'DROP' or 'ACCEPT'. What to do with the packet if it falls in the range.
        """
        self._action = kwargs['action']

    def __call__(self, pywall_packet):
        """
        Filter IP packets.
        
        If some filtering condition on the packet is True, the specified
        action will be returned.
        Subclasses should override filter_condition to get different
        behavior. This method should remain untouched.
        """
        if self.filter_condition(pywall_packet):
            return self._action
        else:
            return False

class IPRangeRule(IPRule):
    """Filter IP packets based on source/dest address."""
    def __init__(self, **kwargs):
        IPRule.__init__(self, **kwargs)
        self._ip_range = netaddr.IPRange(kwargs['start_ip'], kwargs['end_ip'])

class SourceIPRule(IPRangeRule):
    """Filter IP packets based on source address"""
    def __init__(self, **kwargs):
        IPRangeRule.__init__(self, **kwargs)
    
    def filter_condition(self, pywall_packet):
        """
        Filter packets if their source address falls within the ip_range.
        """
        return pywall_packet._src_ip in self._ip_range

class DestinationIPRule(IPRangeRule):
    """Filter IP packets based on destination address"""
    def __init__(self, **kwargs):
        IPRangeRule.__init__(self, **kwargs)

    def filter_condition(self, pywall_packet):
        """
        Filter packets if their destination address falls within the ip_range."""
        return pywall_packet._dest_ip in self._ip_range
register(SourceIPRule)
register(DestinationIPRule)
