import logging
import os
from os import path
from typing import List

from yabu.exceptions import LocalPathNotWritable, IdentityFileUnreadable, TargetFailed

_LOGGER = logging.getLogger(__package__)


class BackupTask:
    def __init__(self,
                 remote_base_path: str,
                 local_path: str,
                 targets: List[str],
                 identity_file: str = None,
                 delete_old: bool = False,
                 stop_on_failed_target: bool = False,
                 **kwargs):
        self._remote_base_path = remote_base_path
        self._local_path = local_path
        self._targets = targets
        self._identity_file = identity_file
        self._delete_old = delete_old
        self._stop_on_failed_target = stop_on_failed_target

        # creates local directory if necessary
        os.makedirs(self._local_path, exist_ok=True)

        # checks if the local path is writable
        if not os.access(self._local_path, os.W_OK):
            raise LocalPathNotWritable(self._local_path)

        # checks if provided key is readable
        if self._identity_file is not None:
            if not os.access(self._identity_file, os.R_OK):
                raise IdentityFileUnreadable(self._identity_file)

    def start(self):
        for t in self._targets:
            # creates the command for the current target
            command = self.mk_command(t)

            _LOGGER.debug("Run command `{}`".format(command))

            # launches the command
            if os.system(command) != 0:
                _LOGGER.warning("Failed backup_task.py target `{}`".format(command))

                # raises an error if required
                if self._stop_on_failed_target:
                    raise TargetFailed(t)

    def mk_command(self, target: str) -> str:
        # prepares remote path
        if ":" in self._remote_base_path:
            server, base_path = self._remote_base_path.split(":")
            remote_path = "{}:{}".format(server, path.join(base_path, target))
        else:
            remote_path = path.join(self._remote_base_path, target)

        command = ["rsync"]

        # adds necessary flag
        command += ["-a", "--relative"]

        # if provided adds the identity file
        if self._identity_file is not None:
            command += ["-e", "'ssh -i {} -o IdentitiesOnly=yes'".format(self._identity_file)]

        # if required allow delete local files
        if self._delete_old:
            command += ["--delete"]

        # adds the paths
        command += [remote_path, self._local_path]

        return " ".join(command)
