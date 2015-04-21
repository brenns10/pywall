from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
from tcp_connection_test import TCPConnectionTest
from udp_connection_test import UDPConnectionTest

import socket
import select

tests = [
    # Tests src_port filtering
    ('BlockLocalSrcHTTP', TCPConnectionTest('test/block_local_src_web.json', 80, expected_num_connections=0)),
    ('TCPUnregSrcPort1', TCPConnectionTest('test/block_unreg_src_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregSrcPort2', TCPConnectionTest('test/block_unreg_src_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregSrcPort3', TCPConnectionTest('test/block_unreg_src_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalSrcDNS', UDPConnectionTest('test/block_local_src_web.json', 53, expected_num_connections=0)),
    ('UDPUnregSrcPort1', UDPConnectionTest('test/block_unreg_src_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregSrcPort2', UDPConnectionTest('test/block_unreg_src_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregSrcPort3', UDPConnectionTest('test/block_unreg_src_ports.json', 65535, expected_num_connections=0)),

    # Tests dst_port filters
    ('BlockLocalDstHTTP', TCPConnectionTest('test/block_local_dst_web.json', 80, expected_num_connections=0)),
    ('TCPUnregDstPort1', TCPConnectionTest('test/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregDstPort2', TCPConnectionTest('test/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregDstPort3', TCPConnectionTest('test/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalDstDNS', UDPConnectionTest('test/block_local_dst_web.json', 53, expected_num_connections=0)),
    ('UDPUnregDstPort1', UDPConnectionTest('test/block_unreg_dst_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregDstPort2', UDPConnectionTest('test/block_unreg_dst_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregDstPort3', UDPConnectionTest('test/block_unreg_dst_ports.json', 65535, expected_num_connections=0)),

    # Tests combo dst/src_port filters
    ('BlockLocalHTTP', TCPConnectionTest('test/block_local_web.json', 80, expected_num_connections=0)),
    ('TCPUnregPort1', TCPConnectionTest('test/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregPort2', TCPConnectionTest('test/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregPort3', TCPConnectionTest('test/block_unreg_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalDNS', UDPConnectionTest('test/block_local_web.json', 53, expected_num_connections=0)),
    ('UDPUnregPort1', UDPConnectionTest('test/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregPort2', UDPConnectionTest('test/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregPort3', UDPConnectionTest('test/block_unreg_ports.json', 65535, expected_num_connections=0))
]
