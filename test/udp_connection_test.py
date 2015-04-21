#!/usr/bin/env python2

from pywall_test_case import PyWallTestCase
from udp_server_process import UDPServerProcess
import socket


class UDPConnectionTest(PyWallTestCase):
    def __init__(self, config_filename, port, client_timeout=1, server_timeout=5, expected_num_connections=1):
        self.port = port
        self.timeout = client_timeout
        PyWallTestCase.__init__(self, config_filename,
                                UDPServerProcess(port, server_timeout, expected_num_connections))

    def client_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto("hi!", ('localhost', self.port))
        s.close()


tests = [
    ('UDPConnectionTest', UDPConnectionTest('test/tcp_connection.json', 58008, client_timeout=1, server_timeout=5)),
]
