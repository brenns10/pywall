from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
from tcp_connection_test import TCPConnectionTest
from udp_connection_test import UDPConnectionTest

import socket
import select

tests = [
    # Tests src_port filtering
    ('TCPUnregSrcPort1', TCPConnectionTest('test/integration/block_unreg_src_ports.json', 49151, src_port=49251, expected_num_connections=0)),
    ('TCPUnregSrcPort2', TCPConnectionTest('test/integration/block_unreg_src_ports.json', 49152, src_port=49252, expected_num_connections=0)),
    ('TCPUnregSrcPort3', TCPConnectionTest('test/integration/block_unreg_src_ports.json', 65535, src_port=65435, expected_num_connections=0)),
    ('UDPUnregSrcPort1', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 49151, src_port=49251, expected_num_connections=0)),
    ('UDPUnregSrcPort2', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 49152, src_port=49252, expected_num_connections=0)),
    ('UDPUnregSrcPort3', UDPConnectionTest('test/integration/block_unreg_src_ports.json', 65535, src_port=64535, expected_num_connections=0)),

    # Tests dst_port filters
    ('TCPUnregDstPort1', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregDstPort2', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregDstPort3', TCPConnectionTest('test/integration/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),
    ('UDPUnregDstPort1', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregDstPort2', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregDstPort3', UDPConnectionTest('test/integration/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),

    # Tests combo dst/src_port filters
    ('TCPUnregPort1', TCPConnectionTest('test/integration/block_unreg_ports.json', 49151, src_port=49251, expected_num_connections=0)),
    ('TCPUnregPort2', TCPConnectionTest('test/integration/block_unreg_ports.json', 49152, src_port=49252, expected_num_connections=0)),
    ('TCPUnregPort3', TCPConnectionTest('test/integration/block_unreg_ports.json', 65535, src_port=65435, expected_num_connections=0)),
    ('UDPUnregPort1', UDPConnectionTest('test/integration/block_unreg_ports.json', 49151, src_port=49251, expected_num_connections=0)),
    ('UDPUnregPort2', UDPConnectionTest('test/integration/block_unreg_ports.json', 49152, src_port=49252, expected_num_connections=0)),
    ('UDPUnregPort3', UDPConnectionTest('test/integration/block_unreg_ports.json', 65535, src_port=65435, expected_num_connections=0)),
]
