PyWall
======

A Python firewall: Because slow networks are secure networks.

Running
-------

You need Linux, IPTables, Python 2 and the package
[python-netfilterqueue](https://github.com/kti/python-netfilterqueue).  Follow
the installation instructions for that package (you need Python headers and
`libnetfilter_queue` installed), preferably with pip in a virtualenv.

The main file is `pywall.py`.  It needs to be run as root.  So, to run, simply
do `sudo ./pywall.py` (or, more verbosely, `sudo python pywall.py`).  The PyWall
takes care of setting up and tearing down its IPTables rule, so you don't need
to worry about anything.  Once you Control-C it, the IPTables rule should be
deleted, and your internet connection should be unaffected.
