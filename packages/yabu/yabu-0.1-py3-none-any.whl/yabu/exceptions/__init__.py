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


class BackupError(YABUerror):
    pass


class LocalPathNotWritable(BackupError):
    def __init__(self, path: str):
        self._path = path

    def __str__(self) -> str:
        return "Directory '{}' is not writable".format(self._path)


class FailedTarget(BackupError):
    def __init__(self, path: str):
        self._path = path

    def __str__(self) -> str:
        return "Failed sync of '{}'".format(self._path)


class FailedTask(BackupError):
    pass
