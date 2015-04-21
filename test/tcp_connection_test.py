#!/usr/bin/env python2

from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
import socket


class TCPConnectionTest(PyWallTestCase):
    def __init__(self, config_filename, port, client_timeout=1, server_timeout=5):
        self.port = port
        self.timeout = client_timeout
        PyWallTestCase.__init__(self, config_filename, TCPServerProcess(port, server_timeout))

    def client_request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect(('localhost', self.port))
        except socket.timeout:
            return


tests = [
    ('TCPConnectionTest', TCPConnectionTest('test/tcp_connection.json', 58008, client_timeout=1, server_timeout=5)),
]
