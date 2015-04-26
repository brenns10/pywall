from conf import CONF
from pywall_acceptance_test_case import PyWallAcceptanceTestCase
from pywall_acceptance_test_case import BaseListener
import socket


class ExampleListener(BaseListener):
    def __init__(self, host):
        self._port = 9001
        self._timeout = 5
        self._host = host
        self._host_ip = socket.gethostbyname(host)

    def listen(self, queue):
        print('listening')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', self._port))
        sock.listen(5)
        sock.settimeout(self._timeout)
        try:
            print('before loop')
            while True:
                s = sock.accept()
                if s.getpeername() == self._host_ip:
                    queue.put(True)
                    s.close()
                    break
                s.close()
            sock.close()
        except socket.timeout:
            sock.close()
            queue.put(False)
        print('done listening')


class ExampleAcceptanceTest(PyWallAcceptanceTestCase):
    def __init__(self, config, host, key_file=None, remote_args=[]):
        PyWallAcceptanceTestCase.__init__(self, config, host, 'example_test',
                                          remote_args=remote_args,
                                          listener=ExampleListener(CONF['host']), key_file=key_file)


tests = [
    ('ExampleAcceptanceTest', ExampleAcceptanceTest('example_config.json',
                                                    '@'.join([CONF['user'], CONF['host']]),
                                                    key_file=CONF['key_file'],
                                                    remote_args=[CONF['host']])),
]
