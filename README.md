PyWall
======

A Python firewall (for academic purposes).

Running
-------

You need Linux, IPTables, Python 2 and the package
[python-netfilterqueue](https://github.com/kti/python-netfilterqueue).  Follow
the installation instructions for that package (you need Python headers and
`libnetfilter_queue` installed), preferably with pip in a virtualenv.

To start the proof of concept, run:

    $ sudo iptables -I INPUT -j NFQUEUE --queue-num 0
    $ sudo python concept.py

Note that once you've added the IPTables rule, you will not have any internet
access, until the firewall starts.  Once you exit the firewall (Control-C), run
the following command to remove the rule and restore normal operation:

    $ sudo iptables -D INPUT -j NFQUEUE --queue-num 0
