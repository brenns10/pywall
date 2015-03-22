#!/usr/bin/env python2
# Pywall proof of concept.

from __future__ import print_function
import netfilterqueue as nfq


def print_and_accept(pkt):
    print(pkt)
    pkt.accept()


if __name__ == '__main__':
    nfqueue = nfq.NetfilterQueue()
    nfqueue.bind(1, print_and_accept)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print()
