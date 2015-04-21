from rules import register, Rule
import time


class PortScanRule(Rule):

    def __init__(self, **kwargs):
        Rule.__init__(self, **kwargs)
        self._history = dict()
        self._scan_threshold = kwargs.get('scan_threshold', 5)
        self._history_lifetime = kwargs.get('history_lifetime', 30)

    def filter_condition(self, packet):
        self._update_history(packet)
        return len(self._history.get(packet._src_ip, [])) < self._scan_threshold

    def _update_history(self, packet):
        self._cleanup_history()
        if packet._src_ip not in self._history:
            self._history[packet._src_ip] = set()
        self._history[packet._src_ip].add((packet.get_payload()._dst_port, time.time()))

    def _cleanup_history(self):
        for ip, port_history in self._history.iteritems():
            ports_to_clear = set()
            for port, timestamp in port_history:
                if time.time() - timestamp > self._history_lifetime:
                    ports_to_clear.add((port, timestamp))
            port_history.difference_update(ports_to_clear)

register(PortScanRule)
