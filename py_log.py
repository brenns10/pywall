"""Logging code goes here."""

import logging
import time
from logging import StreamHandler, FileHandler
from logutils.queue import QueueHandler, QueueListener


def _get_formatter():
    return logging.Formatter(fmt='[%(asctime)s][%(levelname)s] %(message)s')


def initialize_logging(level, queue):

    formatter = _get_formatter()

    logger = logging.getLogger('pywall')
    logger.setLevel(level)

    handler = QueueHandler(queue)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def log_server(level, queue, filename, mode='w'):

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
