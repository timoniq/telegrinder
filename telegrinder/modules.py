import os
import typing

from choicelib import choice_in_order

__all__ = "json", "logger"


class JSONModule(typing.Protocol):
    def loads(self, s: str) -> dict | list:
        ...

    def dumps(self, o: dict | list) -> str:
        ...


class LoggerModule(typing.Protocol):
    def debug(self, __msg: object, *args: object, **kwargs: object):
        ...

    def info(self, __msg: object, *args: object, **kwargs: object):
        ...

    def warning(self, __msg: object, *args: object, **kwargs: object):
        ...

    def error(self, __msg: object, *args: object, **kwargs: object):
        ...

    def critical(self, __msg: object, *args: object, **kwargs: object):
        ...

    def exception(self, __msg: object, *args: object, **kwargs: object):
        ...

    def set_level(self, level: str) -> None:
        ...


logger: LoggerModule
json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
)
logging_module = choice_in_order(["loguru"], default="logging")
logging_level = os.getenv("LOGGER_LEVEL", default="DEBUG").upper()

if logging_module == "loguru":
    import os
    import sys

    from loguru import logger  # type: ignore

    os.environ.setdefault("LOGURU_AUTOINIT", "0")
    log_format = (
        "<level>{level: <8}</level> | "
        "<lg>{time:YYYY-MM-DD HH:mm:ss}</lg> | "
        "<le>{name}</le>:<le>{function}</le>:"
        "<le>{line}</le> > <lw>{message}</lw>"
    )
    logger.remove()  # type: ignore
    handler_id = logger.add(  # type: ignore
        sink=sys.stderr,
        format=log_format,
        enqueue=True,
        colorize=True,
        level=logging_level,
    )

elif logging_module == "logging":
    """
    This is a workaround for lazy formatting with {} in logging.
    About:
    https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
    """
    import inspect
    import logging
    import sys

    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self) -> str:
            return self.fmt.format(*self.args, **self.kwargs)

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
                args = tuple()
            return msg, args, log_kwargs

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(
            "%(name)s | %(levelname)s | %(asctime)s > %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger = logging.getLogger("telegrinder")  # type: ignore
    logger.setLevel(logging.getLevelName(logging_level))  # type: ignore
    logger.addHandler(handler)  # type: ignore
    logger = StyleAdapter(logger)  # type: ignore


def __set_logger_level(level):
    level = level.upper()
    if logging_module == "logging":
        import logging

        logging.getLogger("telegrinder").setLevel(logging.getLevelName(level))
    elif logging_module == "loguru":
        import loguru  # type: ignore

        if loguru.logger._core.handlers:  # type: ignore
            loguru.logger._core.handlers[handler_id]._levelno = loguru.logger.level(level).no  # type: ignore


setattr(logger, "set_level", staticmethod(__set_logger_level))  # type: ignore
