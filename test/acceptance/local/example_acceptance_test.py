from conf import CONF
from pywall_acceptance_test_case import PyWallAcceptanceTestCase
from listeners import TCPListener
import socket


class ExampleAcceptanceTest(PyWallAcceptanceTestCase):
    def __init__(self, config, host, key_file=None, remote_module='', remote_args=[]):
        listener = TCPListener(CONF['remote_host'], CONF['port'])
        PyWallAcceptanceTestCase.__init__(self, config, host,
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=key_file,
                                          listener=listener)

    def run(self):
        return bool(PyWallAcceptanceTestCase.run(self))


tests = [
    ('ExampleAcceptanceTest', ExampleAcceptanceTest('example_config.json',
                                                    '@'.join([CONF['user'], CONF['remote_host']]),
                                                    key_file=CONF['key_file'],
                                                    remote_module='example_test_remote.py',
                                                    remote_args=[CONF['target_host'], str(CONF['port'])])),
]
