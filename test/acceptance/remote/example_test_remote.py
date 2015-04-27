#!/usr/bin/env python2
from __future__ import print_function
import socket
import sys
import time


if __name__ == '__main__':
    print('hello from remote!')
    target_host = socket.gethostbyname(sys.argv[1])
    target_port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9001
    target = (target_host, target_port)
    print('target: %s' % str(target))
    timeout = int(sys.argv[3]) if len(sys.argv) >= 4 else 5

    time.sleep(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(target)
        s.send('knock-knock')
    except socket.timeout:
        print('remote socket timeout')

    print('remote out')
