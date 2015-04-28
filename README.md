PyWall
======

A Python firewall: Because slow networks are secure networks.


Installation
------------

This section assumes that you are installing this program on Ubuntu 14.04 LTS.
This firewall should work on other Linux systems, but safety not guaranteed.

First, install the required packages. On Ubuntu, these are `iptables`, `python`,
`build-essential`, `python-dev`, and `libnetfilter-queue-dev`. Next, use `pip2`
to install the project dependencies, which can be found in `requirements.txt`.

The commands for both these operations are:

    sudo apt-get install build-essential python-dev libnetfilter-queue-dev
    pip install --user -r requirements.txt


Running
-------

The main file is `main.py`, which needs to be run as root to modify IPTables.
Additionally, main needs to receive a JSON configuration file as its first
argument. If running with the example configuration, the command is:

`sudo python2 main.py examples/example.json`

To stop PyWall, press Control-C.


Troubleshooting
---------------

PyWall should undo its changes to IPTables after exiting. However, if you are
unable to access the internet after exiting PyWall, view existing
IPTables rules with `sudo IPTables -nL`. If a rule with the target chain
`NFQueue` lingers, delete it with
`sudo IPTables -D INPUT -j NFQueue --queue-num [undesired-queue-number]`.
