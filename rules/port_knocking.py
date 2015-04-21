from __future__ import print_function
from rules import register
from rules import Rule
from datetime import datetime
from datetime import timedelta
import socket


class PortKnocking(Rule):
    def __init__(self, **kwargs):
        self._port = kwargs.get('port', None)
        self._src_port = kwargs.get('src_port', None)
        self._body = kwargs.get('body' 'knock-knock')
        self._doors = self._convert_doors(kwargs.get('doors', []))
        self._activity = {}  # IP -> (state, timestamp)


    def _convert_doors(self, user_doors):
        final_doors = []
        for proto, port in user_doors:
            if proto == 'TCP' and 0 <= port <= 65535:
                final_doors.append((socket.IPPROTO_TCP, port))
            elif proto == 'UDP' and 0 <= port <= 65535:
                final_doors.append((socket.IPPROTO_UDP, port))
            else:
                raise ValueError('Invalid door: (%s, %d)' % (proto, port))

        if len(final_doors) == 0:
            raise ValueError('No doors given')
        return final_doors

    def filter_condition(self, pywall_packet):
        src_ip = pywall_packet.get_src_ip()
        payload = pywall_packet.get_payload()
        if payload:
            print(payload.get_body())

        i = self._activity.get(src_ip, 0)
        if i < len(self._doors):
            cur_proto, cur_port = self._doors[i]
            if (cur_proto == pywall_packet.get_protocol() and
                cur_port == payload.get_dst_port() and
                self._src_port == payload.get_src_port()):
                i += 1
                self._activity[src_ip] = i
                print('PortKnocking: advance to %d' % i)
                return 'DROP'
            else:
                print('PortKnocking: fall-through')
                return False
        else:
            print('PortKnocking: Accepting from %s' % (src_ip))
            return 'ACCEPT'

    def __call__(self, pywall_packet):
        return self.filter_condition(pywall_packet)


register(PortKnocking)
