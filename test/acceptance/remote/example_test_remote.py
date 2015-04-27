#!/usr/bin/env python2
from __future__ import print_function
import socket
import sys
import time


def rprint(msg):
    """Print a message labelled from remote"""
    print('[REMOTE] %s' % msg)
    

if __name__ == '__main__':
    rprint('hello from remote!')
    target_host = socket.gethostbyname(sys.argv[1])
    target_port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9001
    target = (target_host, target_port)
    rprint('target: %s' % str(target))
    sock_type = sys.argv[3] if len(sys.argv) >= 4 else 'TCP'
    timeout = int(sys.argv[4]) if len(sys.argv) >= 5 else 5

    time.sleep(2)

    if sock_type == 'TCP':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect(target)
            s.send('knock-knock')
        except socket.timeout:
            rprint('remote socket timeout')
    elif sock_type == 'UDP':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        try:
            s.sendto('knock-knock', target)
        except socket.timeout:
            rprint('remote socket timeout')
    else:
        rprint('invalid socket type')

    rprint('remote out')
