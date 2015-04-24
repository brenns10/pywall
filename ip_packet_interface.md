Helpful Links:
- http://www.binarytides.com/raw-socket-programming-in-python-linux/
- http://en.wikipedia.org/wiki/IPv4#Packet_structure

Class definiton: `class IPPacket(Packet):`

Magic Methods:
- `__init__(self, buff)` - parse information out of header, convert payload to TransportLayerPacket if possible
- `__unicode__(self)`    - return printable IP string

Getters:
- `get_src_ip(self)`   - return string version of source IP address
- `get_dst_ip(self)`   - return string version of destination IP address
- `get_protocol(self)` - return protocol value found in IP header
- `get_payload(self)`  - return payload. Should be instance of subclass of
                         TransportLayerPacket if we support the transport layer
                         protocol, raw bytes otherwise
