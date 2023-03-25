import logging
import typing

from choicelib import choice_in_order
from typing_extensions import Protocol


class JSONModule(Protocol):
    def loads(self, s: str) -> dict | list:
        ...

    def dumps(self, o: dict | list) -> str:
        ...


json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
)

logging_module = choice_in_order(["loguru"], default="logging")

if logging_module == "loguru":
    import os
    import sys

    if not os.environ.get("LOGURU_AUTOINIT"):
        os.environ["LOGURU_AUTOINIT"] = "0"
    from loguru import logger  # type: ignore

    if not logger._core.handlers:  # type: ignore
        log_format = (
            "<level>{level: <8}</level> | "
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{name}:{function}:{line} > <level>{message}</level>"
        )
        logger.add(sys.stderr, format=log_format, enqueue=True, colorize=True)

elif logging_module == "logging":
    """
    This is a workaround for lazy formatting with {} in logging.
    About:
    https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
    """
    import inspect
    import logging

    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging.LoggerAdapter):
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, *args, **kwargs):
            if self.isEnabledFor(level):
                msg, args, kwargs = self.proc(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)

        def proc(self, msg, args, kwargs):
            log_kwargs = {
                key: kwargs[key]
                for key in inspect.getfullargspec(self.logger._log).args[1:]
                if key in kwargs
            }
            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = ()
            return msg, args, log_kwargs

    logger = StyleAdapter(logging.getLogger("telegrinder"))  # type: ignore
