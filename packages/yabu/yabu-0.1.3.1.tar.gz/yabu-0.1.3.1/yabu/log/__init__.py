import importlib
import inspect
import logging
import pkgutil
from dataclasses import dataclass
from types import ModuleType
from typing import Union


@dataclass
class LogLevel:
    module: int
    sub_modules: int
    other_modules: int


LOG_LEVELS = [
    LogLevel(logging.INFO, logging.CRITICAL, logging.CRITICAL),
    LogLevel(logging.INFO, logging.ERROR, logging.CRITICAL),
    LogLevel(logging.INFO, logging.WARNING, logging.CRITICAL),
    LogLevel(logging.INFO, logging.INFO, logging.CRITICAL),
    LogLevel(logging.INFO, logging.INFO, logging.WARNING),
    LogLevel(logging.DEBUG, logging.DEBUG, logging.WARNING)
]
_LOGGER = logging.getLogger(__package__)

_log_level: Union[LogLevel, None] = None


def get_log_level() -> Union[LogLevel, None]:
    return _log_level


def logger_setup(log_level: Union[int, LogLevel], base_module: ModuleType = None):
    # if the log level is in int format, converts it in the associated LogLevel
    if isinstance(log_level, int):
        try:
            log_level = LOG_LEVELS[log_level]
        except IndexError:
            log_level = LOG_LEVELS[-1]

    # sets format for the log
    logging.basicConfig(format="%(levelname)s|%(name)s>%(message)s", level=log_level.other_modules)

    # if the base module is not provided retrieves this form the stack
    if base_module is None:
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        base_module = importlib.import_module(mod.__package__)

    # sets log level for the packet
    logging.getLogger(base_module.__package__).setLevel(log_level.module)

    # sets log level for local packages
    for _, modname, _ in pkgutil.walk_packages(path=base_module.__path__,
                                               prefix=base_module.__name__ + ".",
                                               onerror=lambda x: None):
        logging.getLogger(modname).setLevel(log_level.sub_modules)

    _LOGGER.info("Log levels set as {}".format(log_level))

    # saves the log level
    global _log_level
    _log_level = log_level
