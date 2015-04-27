"""
A simple test case that checks whether the connection between remote and target
host is working properly.
"""
from conf import CONF
from pywall_acceptance_test_case import PyWallAcceptanceTestCase
from listeners import TCPListener
from listeners import UDPListener
import socket


class ExampleAcceptanceTestTCP(PyWallAcceptanceTestCase):
    def __init__(self, config, host, key_file=None, remote_module='', remote_args=[]):
        listener = TCPListener(CONF['remote_host'], CONF['port'])
        PyWallAcceptanceTestCase.__init__(self, config, host,
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=key_file,
                                          listener=listener)

    def run(self):
        return bool(PyWallAcceptanceTestCase.run(self))


class ExampleAcceptanceTestUDP(PyWallAcceptanceTestCase):
    def __init__(self, config, host, key_file=None, remote_module='', remote_args=[]):
        listener = UDPListener(CONF['port'])
        PyWallAcceptanceTestCase.__init__(self, config, host,
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=key_file,
                                          listener=listener)

    def run(self):
        return bool(PyWallAcceptanceTestCase.run(self))



tests = [
    ('ExampleAcceptanceTest', ExampleAcceptanceTestTCP('example_config.json',
                                                       '@'.join([CONF['user'], CONF['remote_host']]),
                                                       key_file=CONF['key_file'],
                                                       remote_module='example_test_remote.py',
                                                       remote_args=[CONF['target_host'], str(CONF['port'])])),
    ('ExampleAcceptanceTest', ExampleAcceptanceTestUDP('example_config.json',
                                                       '@'.join([CONF['user'], CONF['remote_host']]),
                                                       key_file=CONF['key_file'],
                                                       remote_module='example_test_remote.py',
                                                       remote_args=[CONF['target_host'], str(CONF['port']),'UDP'])),

]
