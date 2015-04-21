from pywall_test_case import PyWallTestCase
from tcp_server_process import TCPServerProcess
from tcp_connection_test import TCPConnectionTest
from udp_connection_test import UDPConnectionTest

import socket
import select

tests = [
    ('BlockLocalHTTP', TCPConnectionTest('test/block_local_web.json', 80, expected_num_connections=0)),
    ('TCPUnregisteredPort1', TCPConnectionTest('test/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('TCPUnregisteredPort2', TCPConnectionTest('test/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('TCPUnregisteredPort3', TCPConnectionTest('test/block_unreg_ports.json', 65535, expected_num_connections=0)),
    ('BlockLocalDNS', UDPConnectionTest('test/block_local_web.json', 53, expected_num_connections=0)),
    ('UDPUnregisteredPort1', UDPConnectionTest('test/block_unreg_ports.json', 49151, expected_num_connections=0)),
    ('UDPUnregisteredPort2', UDPConnectionTest('test/block_unreg_ports.json', 49152, expected_num_connections=0)),
    ('UDPUnregisteredPort3', UDPConnectionTest('test/block_unreg_ports.json', 65535, expected_num_connections=0)),
]
