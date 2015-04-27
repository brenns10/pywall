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
    if len(sys.argv) >= 5:
        target_host = socket.gethostbyname(sys.argv[1])
        target_port = int(sys.argv[2])
        target = (target_host, target_port)
 
        timeout = 5
        sock_type = sys.argv[3]
        port_type = sys.argv[4]

        time.sleep(2)

        if sock_type == 'TCP':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            if port_type == 'src':
                s.bind(('', target_port))
            try:
                s.connect(target)
                s.send('knock-knock')
            except socket.timeout:
                rprint('remote socket timeout')
            s.close()
        elif sock_type == 'UDP':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            if port_type == 'src':
                s.bind(('', target_port))
            try:
                s.sendto('knock-knock', target)
            except socket.timeout:
                rprint('remote socket timeout')
            s.close()
        else:
            rprint('invlaid socket type')
    else:
        rprint('Insufficient number of args: %d' % len(sys.argv))
    rprint('remote out')
