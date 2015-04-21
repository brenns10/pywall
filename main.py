#!/usr/bin/env python2
"""Main function for PyWall."""

from __future__ import print_function
import sys
import multiprocessing as mp

import config
import egress
import contrack


def run_pywall(conf, packet_queue, query_pipe, kwargs):
    cfg = config.PyWallConfig(conf)
    the_wall = cfg.create_pywall(packet_queue, query_pipe)
    the_wall.run(**kwargs)


def run_egress(packet_queue):
    ct = egress.PyWallEgress(packet_queue)
    ct.run()


def main(conf, **kwargs):
    egress_queue = mp.Queue()
    ingress_queue = mp.Queue()
    query_pywall, query_contrack = mp.Pipe()

    ct = contrack.PyWallConTracker(ingress_queue, egress_queue, query_contrack)

    egress_process = mp.Process(target=run_egress, args=(egress_queue,))
    egress_process.start()
    pywall_process = mp.Process(target=run_pywall, args=(conf, ingress_queue,
                                                         query_pywall, kwargs))
    pywall_process.start()

    ct.run()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: %s CONFIG-FILE" % (sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
