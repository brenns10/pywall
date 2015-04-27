from conf import CONF
from pywall_acceptance_test_case import PyWallAcceptanceTestCase
from listeners import TCPListener
from listeners import UDPListener
import socket


class TestBlockTCP(PyWallAcceptanceTestCase):
    def __init__(self, config, key_file=None, remote_module='', remote_args=[]):
        listener = TCPListener(CONF['remote_host'], CONF['port'])
        PyWallAcceptanceTestCase.__init__(self, config, '@'.join([CONF['user'], CONF['remote_host']]),
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=CONF['key_file'],
                                          listener=listener)

    def run(self):
        return not bool(PyWallAcceptanceTestCase.run(self))


class TestBlockUDP(PyWallAcceptanceTestCase):
    def __init__(self, config, key_file=None, remote_module='', remote_args=[]):
        listener = UDPListener(CONF['port'])
        PyWallAcceptanceTestCase.__init__(self, config, '@'.join([CONF['user'], CONF['remote_host']]),
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=CONF['key_file'],
                                          listener=listener)

    def run(self):
        return not bool(PyWallAcceptanceTestCase.run(self))


tests = [
    # Tests dst_port filtering
    ('TCPUnregDstPort1', TestBlockTCP('block_unreg_dst_ports.json',
                                      remote_module='example_test_remote.py',
                                      remote_args=[CONF['target_host'], str(49152)])),
    ('UDPUnregDstPort1', TestBlockUDP('block_unreg_dst_ports.json',
                                      remote_module='example_test_remote.py',
                                      remote_args=[CONF['target_host'], str(49152), 'UDP'])),
]

s = '''
    ('TCPUnregSrcPort2', TCPConnectionTest('test/integration/block_unreg_src_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregSrcPort3', TCPConnectionTest('test/integration/block_unreg_src_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalSrcDNS', UDPConnectionTest('test/integration/block_local_src_web.json', 53, expected_num_connections=0)),
    ('UDPUnregSrcPort1', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregSrcPort2', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregSrcPort3', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 65535, expected_num_connections=0)),

    # Tests dst_port filters
    ('BlockLocalDstHTTP', TCPConnectionTest('test/integration/block_local_dst_web.json', 80, expected_num_connections=0)),
    ('TCPUnregDstPort1', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregDstPort2', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregDstPort3', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalDstDNS', UDPConnectionTest('test/integration/block_local_dst_web.json', 53, expected_num_connections=0)),
    ('UDPUnregDstPort1', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregDstPort2', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregDstPort3', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),

    # Tests combo dst/src_port filters
    ('BlockLocalHTTP', TCPConnectionTest('test/integration/block_local_web.json', 80, expected_num_connections=0)),
    ('TCPUnregPort1', TCPConnectionTest('test/integration/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregPort2', TCPConnectionTest('test/integration/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregPort3', TCPConnectionTest('test/integration/block_unreg_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalDNS', UDPConnectionTest('test/integration/block_local_web.json', 53, expected_num_connections=0)),
    ('UDPUnregPort1', UDPConnectionTest('test/integration/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregPort2', UDPConnectionTest('test/integration/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregPort3', UDPConnectionTest('test/integration/block_unreg_ports.json', 65535, expected_num_connections=0))
]
'''
