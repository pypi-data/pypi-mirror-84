from __future__ import annotations

import logging
from os import path
from shutil import which
from typing import Dict

import yamale
from yamale import YamaleError
from yaml.scanner import ScannerError

from yabu import exceptions, BackupTask
from yabu.exceptions import BackupTaskError, TaskFailed

_LOGGER = logging.getLogger(__package__)


class YABU:
    def __init__(self,
                 tasks: Dict[str, Dict],
                 stop_on_failed_task: bool = False,
                 **kwargs):
        self._tasks = tasks
        self._stop_on_failed_task = stop_on_failed_task

        # Checks if the necessary system tools are available
        YABU._check_tools()

    @classmethod
    def make_from_config(cls, config_path: str, **kwargs) -> YABU:
        # Loads the config schema to validate the config
        schema = yamale.make_schema(path.join(path.dirname(__file__), "resources/config.schema.yaml"))

        # Tries to load config file
        try:
            config = yamale.make_data(config_path)
        except FileNotFoundError:
            _LOGGER.error("Configuration file '{}' not found".format(config_path))
            raise exceptions.ConfigNotFound(config_path)
        except ScannerError as e:
            _LOGGER.error("Invalid configuration file '{}'\n{}".format(config_path, e))
            raise exceptions.InvalidConfig(e)

        # Tries to validate the configuration with the schema
        try:
            yamale.validate(schema, config)
        except YamaleError as e:
            _LOGGER.error("Invalid configuration file '{}'\n{}".format(config_path, e))
            raise exceptions.InvalidConfig(e)

        _LOGGER.info("Configuration loaded")

        # create instance form config
        config, _ = config[0]
        return cls(**config, **kwargs)

    @staticmethod
    def _check_tools() -> None:
        # Checks if 'rsync' is available
        if which("rsync") is None:
            e = exceptions.RsyncNotAvailable
            _LOGGER.error(e)
            raise e

        _LOGGER.info("All the needed tools are available")

    def start(self):
        for name, config in self._tasks.items():
            try:
                bi = BackupTask(**config)

                _LOGGER.info("Created backup instance for {}".format(name))

                bi.start()

            except BackupTaskError as e:
                _LOGGER.error("Task {} failed\n{}".format(name, e))

                if self._stop_on_failed_task:
                    raise TaskFailed(e)
