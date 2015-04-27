#!/usr/bin/env python2
"""TCP Connection Tracking."""

from __future__ import print_function

import select
import logging


class PyWallCracker(object):
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
        """Create an instance of the Cracker, given three IPC's.

        - ingress_queue - Queue of flags from ingress TCP packets.
        - egress_queue  - Queue of flags from egress TCP packets.
        - query_pipe    - Pipe for queries and responses from PyWall.
        """
        self.ingress_queue = ingress_queue
        self.egress_queue = egress_queue
        self.query_pipe = query_pipe
        self.connections = {}

    def handle_ingress(self, report):
        """Handle an ingress packet 'report'.

        Updates the state table for the given packet and flags by following our
        TCP state diagram (only including transitions for ingress packets).

        """
        tup, syn, ack, fin = report
        curr = self.connections.get(tup, 'CLOSED')
        l = logging.getLogger('pywall.contrack')
        new = None
        if curr == "CLOSED":
            if syn:
                new = 'SYN_RCVD1'
            else:  # Otherwise, assume this was started before firewall ran.
                new = 'ESTABLISHED'
        elif curr == 'SYN_RCVD2':
            if ack:
                new = 'ESTABLISHED'
        elif curr == 'SYN_SENT1':
            if syn and ack:
                new = 'SYN_SENT2'
            elif syn:
                new = 'SYN_SENT3'
        elif curr == 'ESTABLISHED':
            if fin:
                new = 'CLOSE_WAIT1'
            else:
                new = 'ESTABLISHED'
        elif curr == 'FIN_WAIT_1':
            if fin and ack:
                new = 'FIN_WAIT_3'
            elif ack:
                new = 'FIN_WAIT_2'
            elif fin:
                new = 'CLOSING'
        elif curr == 'FIN_WAIT_2':
            if fin:
                new = 'FIN_WAIT_3'
        elif curr == 'CLOSING':
            if ack:
                new = 'FIN_WAIT_3'
        elif curr == 'CLOSING2':
            if ack:
                new = 'CLOSED'
        elif curr == 'LAST_ACK':
            if ack:
                new = 'CLOSED'

        if new is None:
            # Log undefined transitions and don't change the state of the
            # connection.
            new = curr
            l.error('RCV: %r (%s): syn=%r, ack=%r, fin=%r => %s'
                    ' (UNDEFINED TRANSITION)' %
                    (tup, curr, syn, ack, fin, new))
        else:
            # Log other transitions at the lowest level, in case we need to
            # debug.
            l.debug('RCV: %r (%s): syn=%r, ack=%r, fin=%r => %s' %
                    (tup, curr, syn, ack, fin, new))

        # Update the connection status.
        self.connections[tup] = new

    def handle_egress(self, report):
        """Handle an egress packet 'report'.

        Updates the state table for the given packet and flags by following our
        TCP state diagram (only including transitions for egress packets).

        """
        tup, syn, ack, fin = report
        curr = self.connections.get(tup, 'CLOSED')
        l = logging.getLogger('pywall.contrack')
        new = None
        if curr == 'CLOSED':
            if syn:
                new = 'SYN_SENT1'
            else:  # Assume this was running before hand.
                new = 'ESTABLISHED'
        elif curr == 'SYN_SENT1':
            if syn:
                new = 'SYN_SENT1'  # This means we are retrying a connection.
        elif curr == 'SYN_RCVD1':
            if syn and ack:
                new = 'SYN_RCVD2'
        elif curr == 'SYN_RCVD2':
            if fin:
                new = 'FIN_WAIT_1'
        elif curr == 'SYN_SENT3':
            if ack:
                new = 'SYN_RCVD2'
        elif curr == 'SYN_SENT2':
            if ack:
                new = 'ESTABLISHED'
        elif curr == 'ESTABLISHED':
            if fin:
                new = 'FIN_WAIT_1'
            else:
                new = 'ESTABLISHED'
        elif curr == 'CLOSE_WAIT1':
            if fin and ack:
                new = 'LAST_ACK'
            elif ack:
                new = 'CLOSE_WAIT2'
        elif curr == 'CLOSE_WAIT2':
            if fin:
                new = 'LAST_ACK'
        elif curr == 'CLOSING':
            if ack:
                new = 'CLOSING2'
        elif curr == 'FIN_WAIT_3':
            if ack:
                new = 'CLOSED'

        if new is None:
            # Log undefined transitions and don't change the state of the
            # connection.
            new = curr
            l.error('SND: %r (%s): syn=%r, ack=%r, fin=%r => %s'
                    ' (UNDEFINED TRANSITION)' %
                    (tup, curr, syn, ack, fin, new))
        else:
            # Log other transitions at the lowest level, in case we need to
            # debug.
            l.debug('SND: %r (%s): syn=%r, ack=%r, fin=%r => %s' %
                    (tup, curr, syn, ack, fin, new))

        self.connections[tup] = new

    def handle_query(self, con_tuple):
        """Take a query, load the state, and return it in the query pipe."""
        self.query_pipe.send(self.connections.get(con_tuple, 'CLOSED'))

    def run(self):
        """Run the connection tracking process.

        Selects on the IPC, waiting for input.
        """
        while True:
            egress_fd = self.egress_queue._reader.fileno()
            ingress_fd = self.ingress_queue._reader.fileno()
            query_fd = self.query_pipe.fileno()

            # Use select to get a list of file descriptors ready to be read.
            ready, _, _ = select.select([egress_fd, ingress_fd, query_fd], [], [])
            for ready_fd in ready:
                if ready_fd == egress_fd:
                    egress_packet = self.egress_queue.get_nowait()
                    self.handle_egress(egress_packet)
                elif ready_fd == ingress_fd:
                    ingess_packet = self.ingress_queue.get_nowait()
                    self.handle_ingress(ingess_packet)
                elif ready_fd == query_fd:
                    self.handle_query(self.query_pipe.recv())
