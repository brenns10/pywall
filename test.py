#!/usr/bin/env python2
"""Test bench for PyWall."""

from __future__ import print_function
import multiprocessing as mp
import socket
import os
import signal
import time
import select


def run_pywall(config_file, **kwargs):
    import pywall
    from config import PyWallConfig
    pywall._NFQ_INIT = 'iptables -I INPUT -i lo -j NFQUEUE --queue-num %d'
    pywall._NFQ_CLOSE = 'iptables -D INPUT -i lo -j NFQUEUE --queue-num %d'
    conf = PyWallConfig(config_file)
    wall = conf.create_pywall()
    wall.run(**kwargs)


class ServerProcess(object):
    def run(self, q):
        self.setup_socket()
        res = self.wait_socket()
        print('after wait_socket')
        q.put(res)
        print('put in queue')


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


class PyWallTestCase(object):
    def __init__(self, config_filename, server, server_sleep_time=1):
        self.config_filename = config_filename
        self.server_sleep_time = server_sleep_time
        self.set_server(server)

    def set_server(self, server):
        self.queue = mp.Queue()
        self.server = server
        self.server_process = mp.Process(target=server.run,
                                          args=(self.queue,))

    def run(self):
        sem = mp.Semaphore(0)
        self.wall_process = mp.Process(target=run_pywall,
                                       args=(self.config_filename,), kwargs={'test':True, 'lock':sem})
        self.wall_process.start()
        sem.acquire()  # firewall is ready here
        self.server_process.start()
        time.sleep(self.server_sleep_time)
        self.client_request()
        self.server_process.join()
        if self.queue.get():
            print('TEST PASSED')
        else:
            print('TEST FAILED')
        os.kill(self.wall_process.pid, signal.SIGINT)
        self.wall_process.join()
        print('Test over')


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


if __name__ == '__main__':
    print('hi')
    test = TCPConnectionTest('test/tcp_connection.json', 58008, client_timeout=1, server_timeout=5)
    test.run()
