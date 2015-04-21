#!/usr/bin/env python2
"""TCP Connection Tracking."""

from __future__ import print_function
from packets import IPPacket, TCPPacket

import os

import netfilterqueue as nfq


class PyWallConTracker(object):

    def __init__(self, mp_queue, queue_num=2, test=False):
        self.queue_num = queue_num
        self.mp_queue = mp_queue
        self._nfq_init = 'iptables -I OUTPUT -j NFQUEUE --queue-num %d'
        self._nfq_close = 'iptables -D OUTPUT -j NFQUEUE --queue-num %d'
        if test:
            self._nfq_init = 'iptables -I OUTPUT -i lo -j NFQUEUE --queue-num %d'
            self._nfq_close = 'iptables -D OUTPUT -i lo -j NFQUEUE --queue-num %d'
        self.connections = {}

    def run(self):
        setup = self._nfq_init % self.queue_num
        teardown = self._nfq_close % self.queue_num

        os.system(setup)
        print('Set up IPTables: ' + setup)

        nfqueue = nfq.NetfilterQueue()
        nfqueue.bind(self.queue_num, self.callback)
        try:
            nfqueue.run()
        finally:
            os.system(teardown)
            print('\nTore down IPTables: ' + teardown + '\n')

    def callback(self, packet):
        # Parse packet
        ip_packet = IPPacket(packet.get_payload())
        tcp_packet = ip_packet.get_payload()

        # Accept non-TCP packets.
        if type(tcp_packet) is not TCPPacket:
            packet.accept()
            return

        # Attempt to follow along with the TCP state diagram (with only one side
        # of the communication).
        tup = (ip_packet._src_ip, tcp_packet._src_port, ip_packet._dest_ip,
               tcp_packet._dest_port)
        curr = self.connections.get(tup, 'CLOSED')
        if curr == 'CLOSED':
            if tcp_packet.flag_syn:
                new = 'SYN_SENT'
            else:
                new = 'ESTABLISHED'
                print('Outbound packet in closed connection, entering ESTABLISHED.')
        elif curr == 'SYN_SENT':
            if not tcp_packet.flag_fin:
                new = 'ESTABLISHED'
            else:
                new = 'CLOSED'
        elif curr == 'ESTABLISHED':
            if tcp_packet.flag_fin:
                # Remote is closing connection.
                new = 'CLOSE_WAIT'
            else:
                new = 'ESTABLISHED'
        elif curr == 'CLOSE_WAIT':
            new = 'CLOSED'
        else:
            new = 'CLOSED'

        print('%r, state=%s: SYN=%r, ACK=%r, FIN=%r, new=%s' %
              (tup, curr, bool(tcp_packet.flag_syn), bool(tcp_packet.flag_ack),
               bool(tcp_packet.flag_fin), new))
        # Update pywall on the new connection state.
        if curr != new:
            #self.mp_queue.put((tup, new))
            pass
        self.connections[tup] = new
        #print(self.connections)
        packet.accept()


def run_contrack(queue):
    ct = PyWallConTracker(queue)
    ct.run()
