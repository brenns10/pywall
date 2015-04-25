#!/usr/bin/env python2
"""Contains PyWall class, the main class for our Python firewall."""

from __future__ import print_function
from packets import IPPacket, TCPPacket, to_tuple

import os
import logging

import netfilterqueue as nfq

_NFQ_INIT = 'iptables -I INPUT -j NFQUEUE --queue-num %d'
_NFQ_CLOSE = 'iptables -D INPUT -j NFQUEUE --queue-num %d'
_pipe = 'Yo'


def get_pipe():
    global _pipe
    return _pipe


class PyWall(object):
    """The main class for PyWall.

    This class contains all rules for the firewall.  Furthermore, it waits on
    NetfilterQueue for packets, runs them through rules, and ultimately accepts
    or drops the packets.
    """

    def __init__(self, tcp_queue, query_pipe, queue_num=1, default='DROP'):
        """Create a PyWall object, specifying NFQueue queue number."""
        global _pipe
        _pipe = query_pipe
        self.queue_num = queue_num
        self.tcp_queue = tcp_queue
        self.query_pipe = query_pipe
        self.chains = {'INPUT': [], 'ACCEPT': None, 'DROP': None}
        self.default = default
        self._start = 'INPUT'
        self._old_handler = None

    def add_chain(self, chain_name):
        """Add a new, empty chain."""
        self.chains[chain_name] = []

    def add_rule(self, chain, rule):
        """Add a rule to a chain."""
        self.chains[chain].append(rule)

    def _apply_chain(self, chain, nfqueue_packet, pywall_packet):
        """Run the packet through a chain."""
        l = logging.getLogger('pywall.pywall')
        if chain == 'ACCEPT':
            payload = pywall_packet.get_payload()
            # We don't want to tell the connection tracker that we've accepted a
            # TCP connection until we're sure that we have.
            l.debug('ACCEPT %s' % unicode(pywall_packet))
            if type(payload) is TCPPacket:
                tup = to_tuple(pywall_packet)
                if self.tcp_queue is not None:
                    self.tcp_queue.put((tup, bool(payload.flag_syn),
                                        bool(payload.flag_ack),
                                        bool(payload.flag_fin)))
            nfqueue_packet.accept()
        elif chain == 'DROP':
            l.info('DROP %s' % unicode(pywall_packet))
            nfqueue_packet.drop()
        else:
            # Match against every rule:
            for rule in self.chains[chain]:
                result = rule(pywall_packet)
                # If it matches, execute the rule.
                if result:
                    return self._apply_chain(result, nfqueue_packet,
                                             pywall_packet)
            # If no matches, run the default rule.
            return self._apply_chain(self.default, nfqueue_packet,
                                     pywall_packet)

    def callback(self, packet):
        """Accept packets from NFQueue."""
        pywall_packet = IPPacket(packet.get_payload())
        self._apply_chain(self._start, packet, pywall_packet)

    def run(self, **kwargs):
        """Run the PyWall!"""
        # Setup firewall rule.
        setup = _NFQ_INIT % self.queue_num
        os.system(setup)
        print('Set up IPTables: ' + setup)

        # Bind and run NFQ.
        nfqueue = nfq.NetfilterQueue()
        nfqueue.bind(self.queue_num, self.callback)
        if kwargs.get('test', False):
            lock = kwargs.get('lock', None)
            if lock:
                lock.release()

        try:
            nfqueue.run()
        except KeyboardInterrupt:
            pass
        finally:
            # Always remove the firewall rule when we're done.
            teardown = _NFQ_CLOSE % self.queue_num
            os.system(teardown)
            print('\nTore down IPTables: ' + teardown)
