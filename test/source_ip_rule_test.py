from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
import socket
import select


class SourceIPRuleTest(PyWallTestCase):
    def __init__(self, config_filename, port, client_timeout=1, server_timeout=5, expected_num_connections=1):
        self.port = port
        self.timeout = client_timeout
        PyWallTestCase.__init__(self, config_filename, TCPServerProcess(port, server_timeout, expected_num_connections))

    def client_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect(('localhost', self.port))
        except socket.timeout:
            return
        finally:
            s.close()


tests = [
    ('SourceIPRuleOutOfRangeTest', SourceIPRuleTest('test/source_ip_rule_out_of_range.json', 58008, client_timeout=1, server_timeout=5)),
    ('SourceIPRuleInRangeAcceptTest', SourceIPRuleTest('test/source_ip_rule_in_range_accept.json', 58008, client_timeout=1, server_timeout=5)),
    ('SourceIPRuleInRangeDropTest', SourceIPRuleTest('test/source_ip_rule_in_range_drop.json', 58008, client_timeout=1, server_timeout=5, expected_num_connections=0)),
]
