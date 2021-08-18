"""
Copyright 2021 Charles McMarrow
"""

# built-in
import logging

LOG = logging.getLogger("dual_tape")
LOG_HANDLER = logging.StreamHandler()
LOG_FORMATTER = logging.Formatter('[%(asctime)s] %(message)s')
LOG_HANDLER.setFormatter(LOG_FORMATTER)
LOG.addHandler(LOG_HANDLER)
LOG_RUNNING = False


def enable_log() -> None:
    """
    info: Turns on logging an sets log level.
    :return: None
    """
    global LOG_RUNNING
    LOG_RUNNING = True
    LOG.setLevel(logging.DEBUG)


def log(message: str) -> None:
    """
    info: Logs message.
    :param message: str
    :return: None
    """
    if LOG_RUNNING:
        LOG.debug(message)
