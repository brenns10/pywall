from conf import CONF
from pywall_acceptance_test_case import PyWallAcceptanceTestCase
from listeners import TCPListener
from listeners import UDPListener
import socket


class TestBlockTCP(PyWallAcceptanceTestCase):
    def __init__(self, config, port=9001, key_file=None, remote_module='', remote_args=[]):
        listener = TCPListener(CONF['remote_host'], port)
        PyWallAcceptanceTestCase.__init__(self, config, '@'.join([CONF['user'], CONF['remote_host']]),
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=CONF['key_file'],
                                          listener=listener)

    def run(self):
        return not bool(PyWallAcceptanceTestCase.run(self))


class TestBlockUDP(PyWallAcceptanceTestCase):
    def __init__(self, config, port=9001, key_file=None, remote_module='', remote_args=[]):
        listener = UDPListener(port)
        PyWallAcceptanceTestCase.__init__(self, config, '@'.join([CONF['user'], CONF['remote_host']]),
                                          remote_module=remote_module,
                                          remote_args=remote_args,
                                          key_file=CONF['key_file'],
                                          listener=listener)

    def run(self):
        return not bool(PyWallAcceptanceTestCase.run(self))


tests = [
    # Tests destination port filtering
    ('TCPUnregDstPort1', TestBlockTCP('block_unreg_dst_ports.json', 49151,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49151), 'TCP', 'dst'])),
    ('TCPUnregDstPort2', TestBlockTCP('block_unreg_dst_ports.json', 49152,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49152), 'TCP', 'dst'])),
    ('TCPUnregDstPort3', TestBlockTCP('block_unreg_dst_ports.json', 65535,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(65535), 'TCP', 'dst'])),
    ('UDPUnregDstPort1', TestBlockUDP('block_unreg_dst_ports.json', 49151,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49151), 'UDP', 'dst'])),
    ('UDPUnregDstPort2', TestBlockUDP('block_unreg_dst_ports.json', 49152,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49152), 'UDP', 'dst'])),
    ('UDPUnregDstPort3', TestBlockUDP('block_unreg_dst_ports.json', 65535,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(65535), 'UDP', 'dst'])),

    # Test source port filtering
    ('TCPUnregSrcPort1', TestBlockTCP('block_unreg_src_ports.json', 49151,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49151), 'TCP', 'src'])),
    ('TCPUnregSrcPort2', TestBlockTCP('block_unreg_src_ports.json', 49152,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49152), 'TCP', 'src'])),
    ('TCPUnregSrcPort3', TestBlockTCP('block_unreg_src_ports.json', 65535,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(65535), 'TCP', 'src'])),
    ('UDPUnregSrcPort1', TestBlockUDP('block_unreg_src_ports.json', 49151,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49151), 'UDP', 'src'])),
    ('UDPUnregSrcPort2', TestBlockUDP('block_unreg_src_ports.json', 49152,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(49152), 'UDP', 'src'])),
    ('UDPUnregSrcPort3', TestBlockUDP('block_unreg_src_ports.json', 65535,
                                      remote_module='port_filter_remote.py',
                                      remote_args=[CONF['target_host'], str(65535), 'UDP', 'src'])),

    # Conbined source/dstination port filtering
    ('TCPUnregPort1', TestBlockTCP('block_unreg_ports.json', 49151,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(49151), 'TCP', 'src'])),
    ('TCPUnregPort2', TestBlockTCP('block_unreg_ports.json', 49152,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(49152), 'TCP', 'src'])),
    ('TCPUnregPort3', TestBlockTCP('block_unreg_ports.json', 65535,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(65535), 'TCP', 'src'])),
    ('UDPUnregPort1', TestBlockUDP('block_unreg_ports.json', 49151,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(49151), 'UDP', 'src'])),
    ('UDPUnregPort2', TestBlockUDP('block_unreg_ports.json', 49152,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(49152), 'UDP', 'src'])),
    ('UDPUnregPort3', TestBlockUDP('block_unreg_ports.json', 65535,
                                   remote_module='port_filter_remote.py',
                                   remote_args=[CONF['target_host'], str(65535), 'UDP', 'src'])),

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
