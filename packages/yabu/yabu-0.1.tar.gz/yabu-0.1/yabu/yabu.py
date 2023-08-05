from __future__ import annotations

import logging
import os
from os import path
from shutil import which
from typing import List, Dict

import yamale
from yamale import YamaleError
from yaml.scanner import ScannerError

from yabu import exceptions
from yabu.exceptions import FailedTarget

_LOGGER = logging.getLogger(__package__)


class BackupInstance:
    def __init__(self,
                 remote_base_path: str,
                 local_path: str,
                 targets: List[str],
                 delete_old: bool = False,
                 stop_on_failed_target: bool = False,
                 **kwargs):
        self._remote_base_path = remote_base_path
        self._local_path = local_path
        self._targets = targets
        self._delete_old = delete_old
        self._stop_on_failed_target = stop_on_failed_target

        # creates local directory if necessary
        os.makedirs(self._local_path, exist_ok=True)

        # checks if the local path is writable
        if not os.access(self._local_path, os.W_OK):
            raise exceptions.LocalPathNotWritable(self._local_path)

    def start(self):
        for t in self._targets:
            # prepares remote path
            if ":" in self._remote_base_path:
                server, base_path = self._remote_base_path.split(":")
                remote_path = "{}:{}".format(server, path.join(base_path, t))
            else:
                remote_path = path.join(self._remote_base_path, t)

            command = ["rsync", "-a", "--relative"]

            if self._delete_old:
                command += ["--delete"]

            command += [remote_path, self._local_path]

            _LOGGER.debug("Run command `{}`".format(" ".join(command)))

            # launches the command
            if os.system(" ".join(command)) != 0:
                _LOGGER.warning("Failed task target `{}`".format(" ".join(command)))

                # raises an error if required
                if self._stop_on_failed_target:
                    raise FailedTarget(remote_path)


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
            bi = BackupInstance(**config)

            _LOGGER.info("Created backup instance for {}".format(name))

            try:
                bi.start()
            except FailedTarget as e:
                if self._stop_on_failed_task:
                    raise exceptions.FailedTask(e)
