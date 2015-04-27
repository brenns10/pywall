"""Contains code to setup logging, and to run the logger process.

Sadly, logging in multiprocessing programs is not trivial.  Happily, Python
provides wonderful logging utilities that make multiprocessing logging much
nicer to setup.  We use these utilities here.  The external "logutils" module
actually contains logging library items that are present in Python 3,
backported to Python 2.

"""

import logging
import time
from logging import StreamHandler, FileHandler

from logutils.queue import QueueHandler, QueueListener


def _get_formatter():
    """Creates a formatter with our specified format for log messages."""
    return logging.Formatter(fmt='[%(asctime)s][%(levelname)s] %(message)s')


def initialize_logging(level, queue):
    """Setup logging for a process.

    Creates a base logger for pywall.  Installs a single handler, which will
    send packets across a queue to the logger process.  This function should be
    called by each of the three worker processes before they start.

    """
    formatter = _get_formatter()

    logger = logging.getLogger('pywall')
    logger.setLevel(level)

    handler = QueueHandler(queue)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def log_server(level, queue, filename, mode='w'):
    """Run the logging server.

    This listens to the queue of log messages, and handles them using Python's
    logging handlers.  It prints to stderr, as well as to a specified file, if
    it is given.

    """
    formatter = _get_formatter()
    handlers = []

    sh = StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(level)
    handlers.append(sh)

    if filename:
        fh = FileHandler(filename, mode)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        handlers.append(fh)

    listener = QueueListener(queue, *handlers)
    listener.start()

    # For some reason, queuelisteners run on a separate thread, so now we just
    # "busy wait" until terminated.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
