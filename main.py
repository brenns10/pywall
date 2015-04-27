#!/usr/bin/env python2
"""Main function for PyWall."""

from __future__ import print_function
import multiprocessing as mp
import logging
import argparse

import config
import egress
import contrack
from py_log import initialize_logging, log_server


def run_pywall(conf, packet_queue, query_pipe, kwargs):
    logqueue = kwargs.pop('logqueue', mp.Queue())
    loglevel = kwargs.pop('loglevel', logging.INFO)
    initialize_logging(loglevel, logqueue)
    cfg = config.PyWallConfig(conf)
    the_wall = cfg.create_pywall(packet_queue, query_pipe)
    the_wall.erect(**kwargs)


def run_egress(packet_queue, loglevel, logqueue):
    initialize_logging(loglevel, logqueue)
    ct = egress.PyWallEgress(packet_queue)
    ct.run()


def main(conf, loglevel, filename, **kwargs):
    egress_queue = mp.Queue()
    ingress_queue = mp.Queue()
    log_queue = mp.Queue()
    query_pywall, query_contrack = mp.Pipe()
    kwargs['loglevel'] = loglevel
    kwargs['logqueue'] = log_queue
    initialize_logging(loglevel, log_queue)

    ct = contrack.PyWallCracker(ingress_queue, egress_queue, query_contrack)

    log_process = mp.Process(target=log_server, args=(loglevel, log_queue,
                                                      filename))
    log_process.start()
    egress_process = mp.Process(target=run_egress, args=(egress_queue,
                                                         loglevel, log_queue))
    egress_process.start()
    pywall_process = mp.Process(target=run_pywall, args=(conf, ingress_queue,
                                                         query_pywall, kwargs))
    pywall_process.start()

    ct.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Build a PyWall')
    parser.add_argument('config', help='JSON configuration file')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO',
                                                      'WARNING', 'ERROR',
                                                      'CRITICAL'],
                        help='set verbosity of logging', default='INFO')
    parser.add_argument('-f', '--log-file', help='set log file', default=None)
    args = parser.parse_args()
    main(args.config, args.log_level, args.log_file)
