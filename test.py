#!/usr/bin/env python2
"""Test bench for PyWall."""

from __future__ import print_function
import multiprocessing as mp
import socket
import os
import signal

from config import PyWallConfig
import pywall


def run_pywall(config_file):
    pywall._NFQ_INIT = 'iptables -I INPUT -i lo -j NFQUEUE --queue-num %d'
    pywall._NFQ_CLOSE = 'iptables -D INPUT -i lo -j NFQUEUE --queue-num %d'
    conf = PyWallConfig(config_file)
    wall = conf.create_pywall()
    wall.run(test=True)


class ConnectionHandler(object):
    def run(self, q):
        self.setup_socket()
        try:
            s.wait_socket()
            q.put(True)
        except socket.timeout:
            q.put(False)


class TCPConnectionHandler(ConnectionHandler):

    def __init__(self, port, timeout=0.1):
        self.port = port
        self.timeout = timeout

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(1)
        self.sock.settimeout(self.timeout)

    def wait_socket(self):
        self.sock.accept()


class PyWallTest(object):

    def set_filename(self, filename):
        self.filename = filename

    def set_handler(self, handler):
        self.queue = mp.Queue()
        self.handler = handler
        self.handler_process = mp.Process(target=handler.run,
                                          args=(self.queue,))

    def run(self):
        self.wall_process = mp.Process(target=run_pywall,
                                       args=(self.filename,))
        self.wall_process.start()
        self.handler_process.start()
        self.request()
        self.handler_process.join()
        if self.queue.get():
            print('TEST PASSED')
        else:
            print('TEST FAILED')
        os.kill(self.wall_process.pid, signal.SIGINT)
        self.wall_process.join()
        print('Test over')


class TCPConnectTest(PyWallTest):

    def __init__(self):
        self.port = 58008
        self.set_filename('test/tcp_connection.json')
        self.set_handler(TCPConnectionHandler(self.port, 0.1))

    def request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', self.port))


if __name__ == '__main__':
    print('hi')
    test = TCPConnectTest()
    test.run()
