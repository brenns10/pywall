#!/usr/bin/env python2
"""Test bench for PyWall."""

from __future__ import print_function
import multiprocessing as mp
import socket
import os
import signal
import select


def run_pywall(config_file, **kwargs):
    import pywall
    from config import PyWallConfig
    pywall._NFQ_INIT = 'iptables -I INPUT -i lo -j NFQUEUE --queue-num %d'
    pywall._NFQ_CLOSE = 'iptables -D INPUT -i lo -j NFQUEUE --queue-num %d'
    conf = PyWallConfig(config_file)
    wall = conf.create_pywall()
    wall.run(**kwargs)


class ConnectionHandler(object):
    def run(self, q):
        self.setup_socket()
        res = self.wait_socket()
        print('after wait_socket')
        q.put(res)


class TCPConnectionHandler(ConnectionHandler):
    def __init__(self, port, timeout=0.5):
        self.port = port
        self.timeout = timeout

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        self.sock.setblocking(0)
        #self.sock.listen(1)
        self.sock.settimeout(self.timeout)

    def wait_socket(self):
        print('Waiting on handler socket.')
        rlist, _, __ = select.select([self.sock], [], [], self.timeout)
        return (len(rlist) >= 1)


class PyWallTest(object):
    def __init__(self, config_filename, handler):
        self.config_filename = config_filename
        self.set_handler(handler)

    def set_handler(self, handler):
        self.queue = mp.Queue()
        self.handler = handler
        self.handler_process = mp.Process(target=handler.run,
                                          args=(self.queue,))

    def run(self):
        sem = mp.Semaphore(0)
        self.wall_process = mp.Process(target=run_pywall,
                                       args=(self.config_filename,), kwargs={'test':True, 'lock':sem})
        self.wall_process.start()
        print('lock acquiring')
        sem.acquire(True)
        print('lock acquired')
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
    def __init__(self, config_filename, port, timeout=1):
        self.port = port
        self.timeout = timeout
        PyWallTest.__init__(self, config_filename, TCPConnectionHandler(port, timeout=0.1))

    def request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect(('localhost', self.port))
        except socket.timeout:
            return


if __name__ == '__main__':
    print('hi')
    test = TCPConnectTest('test/tcp_connection.json', 58008, timeout=1)
    test.run()
