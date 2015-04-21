#!/usr/bin/env python2

from pywall_test_case import PyWallTestCase, ServerProcess
import socket
import select

class TCPServerProcess(ServerProcess):
    def __init__(self, port, timeout=5):
        self.port = port
        self.timeout = timeout

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(5)

    def wait_socket(self):
        print('Waiting on server socket.')
        rlist, _, __ = select.select([self.sock], [], [], self.timeout)
        return (len(rlist) >= 1)


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
