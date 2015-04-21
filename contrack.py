#!/usr/bin/env python2
"""TCP Connection Tracking."""

from __future__ import print_function

import Queue


class PyWallConTracker(object):
    """Central TCP connection tracking process and class.

    Receives TCP packets from ingress and egress, and updates connection status
    accordingly.  Also, receives connection status queries from the firewall,
    and responds to them.

    Connection tuple is defined as:
    (remote_ip, remote_port, local_ip, local_port)

    Objects placed into the queues should be:
    (connection tuple, syn, ack, fin)

    """

    def __init__(self, ingress_queue, egress_queue, query_pipe):
        self.ingress_queue = ingress_queue
        self.egress_queue = egress_queue
        self.query_pipe = query_pipe
        self.connections = {}

    def handle_ingress(self, report):
        tup, syn, ack, fin = report
        curr = self.connections.get(tup, 'CLOSED')
        new = curr
        if curr == "CLOSED":
            if syn:
                new = 'SYN_RCVD1'
            else:  # Otherwise, assume this was started before firewall ran.
                new = 'ESTABLISHED'
        elif curr == 'SYN_RCVD2':
            if ack:
                new = 'ESTABLISHED'
            else:
                new = curr
                print('INVALID: (SYN_RCVD2)')
        elif curr == 'SYN_SENT1':
            if syn and ack:
                new = 'SYN_SENT2'
            elif syn:
                new = 'SYN_SENT3'
            else:
                print('INVALID: (SYN_SENT1)')
                new = curr
        elif curr == 'ESTABLISHED':
            if fin:
                new = 'CLOSE_WAIT1'
            else:
                new = curr
        elif curr == 'FIN_WAIT_1':
            if ack:
                new = 'FIN_WAIT_2'
            elif fin:
                new = 'CLOSING'
            else:
                print('INVALID: (FIN_WAIT_1)')
                new = curr
        elif curr == 'FIN_WAIT_2':
            if fin:
                new = 'FIN_WAIT_3'
            else:
                print('INVALID: (FIN_WAIT_2)')
                new = curr
        elif curr == 'CLOSING':
            if ack:
                new = 'FIN_WAIT_3'
            else:
                print('INVALID: (CLOSING)')
        elif curr == 'CLOSING2':
            if ack:
                new = 'CLOSED'
            else:
                print('INVALID: (CLOSING2)')
        elif curr == 'LAST_ACK':
            if ack:
                new = 'CLOSED'
            else:
                print('INVALID: (LAST_ACK)')
        else:
            print('INVALID (%s)' % curr)
            new = curr
        self.connections[tup] = new
        print('RCV: %r (%s): syn=%r, ack=%r, fin=%r => %s' %
              (tup, curr, syn, ack, fin, new))

    def handle_egress(self, report):
        tup, syn, ack, fin = report
        curr = self.connections.get(tup, 'CLOSED')
        new = curr
        if curr == 'CLOSED':
            if syn:
                new = 'SYN_SENT1'
            else:  # Assume this was running before hand.
                new = 'ESTABLISHED'
        elif curr == 'SYN_RCVD1':
            if syn and ack:
                new = 'SYN_RCVD2'
            else:
                print('INVALID: (SYN_RCVD1)')
                new = curr
        elif curr == 'SYN_RCVD2':
            if fin:
                new = 'FIN_WAIT_1'
            else:
                print('INVALID: (SYN_RCVD2)')
                new = curr
        elif curr == 'SYN_SENT3':
            if ack:
                new = 'SYN_RCVD2'
            else:
                print('INVALID: (SYN_SENT3)')
                new = curr
        elif curr == 'SYN_SENT2':
            if ack:
                new = 'ESTABLISHED'
            else:
                print('INVALID: (SYN_SENT2)')
                new = curr
        elif curr == 'ESTABLISHED':
            if fin:
                new = 'FIN_WAIT_1'
            else:
                new = curr
        elif curr == 'CLOSE_WAIT1':
            if ack:
                new = 'CLOSE_WAIT2'
            else:
                print('INVALID: (CLOSE_WAIT1)')
                new = curr
        elif curr == 'CLOSE_WAIT2':
            if fin:
                new = 'LAST_ACK'
            else:
                print('INVALID: (CLOSE_WAIT2)')
                new = curr
        elif curr == 'CLOSING':
            if ack:
                new = 'CLOSING2'
            else:
                print('INVALID: (CLOSING)')
                new = curr
        elif curr == 'FIN_WAIT_3':
            if ack:
                new = 'CLOSED'
            else:
                print('INVALID: (FIN_WAIT_3)')
                new = curr
        else:
            print('INVALID: (%s)' % curr)
            new = curr
        self.connections[tup] = new
        print('SND: %r (%s): syn=%r, ack=%r, fin=%r => %s' %
              (tup, curr, syn, ack, fin, new))

    def handle_query(self, con_tuple):
        self.query_pipe.send(self.connections.get(con_tuple, 'CLOSED'))

    def run(self):
        while True:
            try:
                egress_packet = self.egress_queue.get_nowait()
                self.handle_egress(egress_packet)
            except Queue.Empty:
                pass

            try:
                ingess_packet = self.ingress_queue.get_nowait()
                self.handle_ingress(ingess_packet)
            except Queue.Empty:
                pass

            if self.query_pipe.poll():
                self.handle_query(self.query_pipe.recv())
