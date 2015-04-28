#!/usr/bin/env python2
"""TCP Packet egress reporter."""

from __future__ import print_function

import os
import logging

import netfilterqueue as nfq

from packets import IPPacket, TCPPacket, to_tuple


class PyWallEgress(object):
    """Egress monitoring process.

    This class/process doesn't perform any packet filtering.  It simply accepts
    egress packets, and reports them to the Cracker if they are TCP.

    """

    def __init__(self, mp_queue, queue_num=2):
        """Create the egress process.

        Takes the mp_queue, which is where we report the TCP packets.  queue-num
        is the iptables queue to bind to.

        """
        self.queue_num = queue_num
        self.mp_queue = mp_queue
        self._nfq_init = 'iptables -I OUTPUT -j NFQUEUE --queue-num %d'
        self._nfq_close = 'iptables -D OUTPUT -j NFQUEUE --queue-num %d'

    def run(self):
        """Run the egress process."""
        # Create IPTables commands.
        setup = self._nfq_init % self.queue_num
        teardown = self._nfq_close % self.queue_num

        # Set up IPTables to receive egress packets.
        os.system(setup)
        print('Set up IPTables: ' + setup)

        # Create and run NFQ.
        nfqueue = nfq.NetfilterQueue()
        nfqueue.bind(self.queue_num, self.callback)
        try:
            nfqueue.run()
        finally:
            # Tear down IPTables rules.
            os.system(teardown)
            print('\nTore down IPTables: ' + teardown + '\n')

    def callback(self, packet):
        """The callback called by IPTables for each egress packet."""
        # Parse packet
        ip_packet = IPPacket(packet.get_payload())
        tcp_packet = ip_packet.get_payload()
        logging.getLogger('pywall.egress').debug(unicode(ip_packet))

        # Accept non-TCP packets.
        if type(tcp_packet) is not TCPPacket:
            packet.accept()
            return

        # Send the packet to the connection tracker.
        tup = to_tuple(ip_packet, flip=True)
        self.mp_queue.put((tup, bool(tcp_packet.flag_syn),
                           bool(tcp_packet.flag_ack),
                           bool(tcp_packet.flag_fin)))
        packet.accept()
