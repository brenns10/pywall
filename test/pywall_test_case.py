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
        time.sleep(self.server_sleep_time)
        sem = mp.Semaphore(0)
        self.wall_process = mp.Process(target=run_pywall,
                                       args=(self.config_filename,), kwargs={'test':True, 'lock':sem})
        self.wall_process.start()
        sem.acquire()  # firewall is ready here
        self.server_process.start()
        time.sleep(self.server_sleep_time)
        self.client_request()
        self.server_process.join()
        passed = self.queue.get()
        os.kill(self.wall_process.pid, signal.SIGINT)
        self.wall_process.join()
        return passed
