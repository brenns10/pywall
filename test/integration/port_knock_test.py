from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
import socket
import time


class PKTest(PyWallTestCase):
    def __init__(self, config_filename, doors, port, src_port):
        self._timeout = 1
        self._doors = doors
        PyWallTestCase.__init__(self, config_filename, TCPServerProcess(port, timeout=(5*self._timeout)))
        self._port = port
        self._src_port = src_port
        self._body = 'knock-knock'

    def client_request(self):
        print(self._doors)
        for proto, port in self._doors:
            print(proto)
            if proto == 'TCP':
                print('prepping tcp')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self._timeout)
                s.bind(('', self._src_port))
                try:
                    s.connect(('', port))
                    s.close()
                except socket.error:
                    # if firewall is doing its job, connection should be refused.
                    pass
            elif proto == 'UDP':
                print('prepping udp')
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(self._timeout)
                s.bind(('', self._src_port))
                s.sendto(self._body, ('', port))
                s.close()
            time.sleep(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self._timeout)
        try:
            s.connect(('localhost', self._port))
        except socket.timeout:
            print('Final socket timeout!!')


tests = [
    ('PortKnockingTest', PKTest('test/integration/port_knocking_test.json', [('TCP', 49001), ('UDP', 49011)], 2222, 9001)),
]
