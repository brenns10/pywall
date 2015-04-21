from __future__ import print_function
from rules import register
from rules import Rule
from datetime import datetime
from datetime import timedelta
import socket


class PortKnocking(Rule):
    def __init__(self, **kwargs):
        self._protocol = self._proto_to_const(kwargs.get('protocol', None))
        self._port = kwargs.get('port', None)
        self._src_port = kwargs.get('src_port', None)
        self._body = kwargs.get('body' 'knock-knock')
        self._timeout = kwargs.get('timeout', 60)
        self._doors = self._convert_doors(kwargs.get('doors', []))
        self._activity = {}  # IP -> (state, timestamp)

    def _proto_to_const(self, protocol_str):
        if protocol_str == 'TCP':
            return socket.IPPROTO_TCP
        elif protocol_str == 'UDP': 
            return socket.IPPROTO_UDP
        else:
            raise ValueError('Missing or invalid protocol')

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
        act_def = (0, datetime.now())
        src_ip = pywall_packet.get_src_ip()
        payload = pywall_packet.get_payload()

        # get the latest activity
        i, last_activity = self._activity.get(src_ip, act_def)
        # clear if we have timed out
        if last_activity + timedelta(seconds=self._timeout) < datetime.now():
            print('PortKnocking: timeout -- fall through: %s' % (src_ip))
            del self._activity[src_ip]
            i, last_activity = act_def

        if i >= len(self._doors):
            if (self._protocol == pywall_packet.get_protocol() and
                self._port == payload.get_dst_port()):
                print('PortKnocking: accepting from %s' % (src_ip))
                return 'ACCEPT'
            else:
                print('PortKnocking: fall through from recognized ip: %s' % (src_ip))
                return False
        else:
            cur_proto, cur_port = self._doors[i]
            if (cur_proto == pywall_packet.get_protocol() and
                cur_port == payload.get_dst_port() and
                self._src_port == payload.get_src_port()):
                i += 1
                self._activity[src_ip] = (i, datetime.now())
                print('PortKnocking: advance to %d' % i)
                return 'DROP'
            else:
                print('PortKnocking: unrecognized -- fall-through')
                return False
              
    def __call__(self, pywall_packet):
        return self.filter_condition(pywall_packet)


register(PortKnocking)
