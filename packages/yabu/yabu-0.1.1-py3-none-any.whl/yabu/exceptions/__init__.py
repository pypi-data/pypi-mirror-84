class YABUerror(Exception):
    pass


class RsyncNotAvailable(YABUerror):
    def __str__(self) -> str:
        return "'rsync' tool not found"


class ConfigError(YABUerror):
    pass


class ConfigNotFound(ConfigError):
    def __init__(self, file: str):
        self._file = file

    def __str__(self) -> str:
        return "Configuration file '{}' not found".format(self._file)


class InvalidConfig(ConfigError):
    pass


class BackupTaskError(YABUerror):
    pass


class LocalPathNotWritable(BackupTaskError):
    def __init__(self, path: str):
        self._path = path

    def __str__(self) -> str:
        return "Directory '{}' is not writable".format(self._path)


class IdentityFileUnreadable(BackupTaskError):
    def __init__(self, file: str):
        self._file = file

    def __str__(self) -> str:
        return "Identity file '{}' is not readable".format(self._file)


class TargetFailed(BackupTaskError):
    def __init__(self, path: str):
        self._path = path

    def __str__(self) -> str:
        return "Failed sync of '{}'".format(self._path)


class TaskFailed(BackupTaskError):
    pass
