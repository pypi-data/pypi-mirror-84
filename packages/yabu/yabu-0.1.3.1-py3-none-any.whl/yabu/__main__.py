#!/usr/bin/env python3
import argparse
import logging
import sys

from yabu import YABU
from yabu.exceptions import ConfigError
from .log import logger_setup

_LOGGER = logging.getLogger(__package__)

if __name__ == "__main__":
    # gets inline arguments
    parser = argparse.ArgumentParser(prog="python -m yabu")

    parser.add_argument("-c", "--config", dest="config_path", default="/etc/yabu/config.yaml",
                        help="configuration file path")
    parser.add_argument("-v", dest="log_level", action="count", default=0,
                        help="number of -v defines level of verbosity")

    # parses args
    args = vars(parser.parse_args())

    # sets verbosity level
    logger_setup(args["log_level"])

    # removes no longer necessary log level from args
    del args["log_level"]

    # creates an instance of YABU
    try:
        yabu = YABU.make_from_config(**args)
    except ConfigError as e:
        _LOGGER.critical("Configuration issue: I give up")
        sys.exit(1)

    _LOGGER.info("YABU is ready to start")

    # starts backup operations
    yabu.start()
