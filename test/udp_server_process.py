from pywall_test_case import ServerProcess

import socket
import select


class UDPServerProcess(ServerProcess):
    def __init__(self, port, timeout=5, expected_num_connections=1):
        self.port = port
        self.timeout = timeout
        self.expected_num_connections = expected_num_connections

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', self.port))

    def wait_socket(self):
        print('Waiting on server socket.')
        rlist, _, __ = select.select([self.sock], [], [], self.timeout)
        print(len(rlist))
        if len(rlist) > 0:
            print(str(rlist[0]))
        self.sock.close()
        return (len(rlist) == self.expected_num_connections)
