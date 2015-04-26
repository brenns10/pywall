#!/usr/bin/env python2
from __future__ import print_function
import socket
import sys


if __name__ == '__main__':
    print('in remote')
    print(len(sys.argv))
    if len(sys.argv) >= 2:
        print(sys.argv[1])
        print(socket.gethostbyname(sys.argv[1]))
    print('hello from remote!')
