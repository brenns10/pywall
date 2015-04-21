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

    def handle_ingress(self, con_tuple):
        pass

    def handle_egress(self, report):
        tup, syn, ack, fin = report
        curr = self.connections.get(tup, 'CLOSED')
        if curr == 'CLOSED':
            if syn:
                new = 'SYN_SENT'
            else:
                new = 'ESTABLISHED'
                print('Outbound packet in closed connection, entering ESTABLISHED.')
        elif curr == 'SYN_SENT':
            if not fin:
                new = 'ESTABLISHED'
            else:
                new = 'CLOSED'
        elif curr == 'ESTABLISHED':
            if fin:
                # Remote is closing connection.
                new = 'CLOSE_WAIT'
            else:
                new = 'ESTABLISHED'
        elif curr == 'CLOSE_WAIT':
            new = 'CLOSED'
        else:
            new = 'CLOSED'
        self.connections[tup] = new

    def handle_query(self, con_tuple):
        return self.connections.get(con_tuple, 'ESTABLISHED')

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
