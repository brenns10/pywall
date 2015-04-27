from rules import register, SimpleRule
from rules.port_filter import PortRangeFilter
from rules.ip_rules import SourceIPRule, DestinationIPRule


class AddressPortRule(SimpleRule):

    def __init__(self, **kwargs):
        SimpleRule.__init__(self, **kwargs)
        self.port_rule = PortRangeFilter(**kwargs)

        source_args = kwargs.copy()
        source_ip = source_args.pop('src_ip', None)
        if source_ip:
            source_args['cidr_range'] = source_ip
            self.ip_src_rule = SourceIPRule(**source_args)
        else:
            self.ip_src_rule = None

        dest_args = kwargs.copy()
        dest_ip = dest_args.pop('dst_ip', None)
        if dest_ip:
            dest_args['cidr_range'] = dest_ip
            self.ip_dst_rule = DestinationIPRule(**dest_args)
        else:
            self.ip_dst_rule = None

    def filter_condition(self, packet):
        res = self.port_rule.filter_condition(packet)
        if self.ip_src_rule:
            res = res and self.ip_src_rule.filter_condition(packet)
        if self.ip_dst_rule:
            res = res and self.ip_dst_rule.filter_condition(packet)
        return res

register(AddressPortRule)
