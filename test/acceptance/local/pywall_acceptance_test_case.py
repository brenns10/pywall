#!/usr/bin/env python2
from __future__ import print_function
from os.path import join as pjoin
from subprocess import Popen
from datetime import timedelta
from datetime import datetime
from abc import ABCMeta
from abc import abstractmethod
import time
import multiprocessing as mp
import Queue
import os
import signal


# copied from test/integraiton/pywall_test_case.py
def run_pywall(config_file, **kwargs):
    import main
    main.run_pywall(config_file, None, None, kwargs)


def Popen_wait(proc, timeout, interval=1):
    start = datetime.now()
    t = timedelta(seconds=timeout)
    while datetime.now() < start + t and proc.poll() is None:
        time.sleep(interval)
    try:
        proc.kill()
    except Exception as e:
        print('In Popen_wait: may not be an actual error')
        print(type(e))
        print(str(e))



class PyWallAcceptanceTestCase(object):
    __metaclass__ = ABCMeta

    def __init__(self, config, host, test_name, remote_args=[], listener=None, key_file=None, timeout=3):
        self._config = pjoin('test/acceptance/local', config)
        self._host = host
        self._test_name = test_name
        self._timeout = timeout
        self._key_file = key_file
        self._listener = listener
        self._remote_args = remote_args

    def run_test_on_host(self, *args):
        cmd = ' '.join(['/usr/bin/env python2',
                       pjoin('pywall/test/acceptance/remote', self._test_name + '_remote.py')
                    ] + list(args))
        ssh_args = ['ssh', self._host,
                '-i', self._key_file,
                cmd,
        ]
        return Popen(ssh_args)
        
    def run(self):
        passed = False

        # set up PyWall
        print('set up PyWall')
        sem = mp.Semaphore(0)
        pywall = mp.Process(target=run_pywall, args=(self._config,), kwargs={'test': True, 'lock': sem})
        pywall.start()
        sem.acquire()  # by here, pywall is running

        # set up listener
        print('set up listener')
        res_queue = mp.Queue()
        listener = mp.Process(target=self._listener.listen, args=(res_queue, sem))
        listener.start()
        sem.acquire()  # by here, listener is ready

        # call out to host
        print('call out to host')
        remote_proc = self.run_test_on_host(*self._remote_args)

        # wait a bit
        print('wait a bit')
        time.sleep(self._timeout)
        
        # merge in listener
        print('merge in listener')
        listener.join()
        try:
            passed = res_queue.get(timeout=1)
        except Queue.Empty as e:
            print(e)
            passed = True

        # merge in host
        print('merge in host')
        Popen_wait(remote_proc, self._timeout)

        # kill pywall
        print('kill pywall')
        os.kill(pywall.pid, signal.SIGINT)
        pywall.join()

        print('returning')
        return passed


class BaseListener(object):
    """
    Base class for listeners. Extend and implement listen() to suit
    your acceptance test.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def listen(self, queue, sem):
        pass
