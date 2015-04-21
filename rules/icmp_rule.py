"""Rule matching ICMP packets."""

from rules import Rule, register
from packets import ICMPPacket


class ICMPRule(Rule):

    def filter_condition(self, pckt):
        return type(pckt.get_payload()) is ICMPPacket


class ICMPTypeCodeRule(ICMPRule):

    def __init__(self, **kwargs):
        ICMPRule.__init__(self, **kwargs)
        self.type = kwargs['type']
        self.codes = kwargs['codes']

    def filter_condition(self, pckt):
        pl = pckt.get_payload()
        return ICMPRule.filter_condition(self, pckt) and \
            pl.type == self.type and pl.code in self.codes


register(ICMPRule)
register(ICMPTypeCodeRule)
