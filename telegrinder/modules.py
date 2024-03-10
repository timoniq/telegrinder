import os
import typing

from choicelib import choice_in_order


class JSONModule(typing.Protocol):
    def loads(self, s: str) -> dict[str, typing.Any] | list[typing.Any]:
        ...

    def dumps(self, o: dict[str, typing.Any] | list[typing.Any]) -> str:
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

    def set_level(
        self,
        level: typing.Literal[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "EXCEPTION",
        ],
    ) -> None:
        ...


logger: LoggerModule
json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="telegrinder.msgspec_json"
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

    import colorama

    colorama.just_fix_windows_console()  # init & fix console

    FORMAT = (
        "<white>{name: <4} |</white> <level>{levelname: <8}</level>"
        " <white>|</white> <green>{asctime}</green> <white>|</white> <level_module>"
        "{module}</level_module><white>:</white><level_func>"
        "{funcName}</level_func><white>:</white><level_lineno>"
        "{lineno}</level_lineno><white> > </white><level_message>"
        "{message}</level_message>"
    )
    COLORS = {
        "red": colorama.Fore.LIGHTRED_EX,
        "green": colorama.Fore.LIGHTGREEN_EX,
        "blue": colorama.Fore.LIGHTBLUE_EX,
        "white": colorama.Fore.LIGHTWHITE_EX,
        "yellow": colorama.Fore.LIGHTYELLOW_EX,
        "magenta": colorama.Fore.LIGHTMAGENTA_EX,
        "cyan": colorama.Fore.LIGHTCYAN_EX,
        "reset": colorama.Style.RESET_ALL,
    }
    LEVEL_SETTINGS = {
        "INFO": {
            "level": "green",
            "level_module": "blue",
            "level_func": "cyan",
            "level_lineno": "green",
            "level_message": "white",
        },
        "DEBUG": {
            "level": "blue",
            "level_module": "yellow",
            "level_func": "green",
            "level_lineno": "cyan",
            "level_message": "blue",
        },
        "WARNING": {
            "level": "yellow",
            "level_module": "red",
            "level_func": "green",
            "level_lineno": "red",
            "level_message": "yellow",
        },
        "ERROR": {
            "level": "red",
            "level_module": "magenta",
            "level_func": "yellow",
            "level_lineno": "green",
            "level_message": "red",
        },
        "CRITICAL": {
            "level": "cyan",
            "level_module": "yellow",
            "level_func": "yellow",
            "level_lineno": "yellow",
            "level_message": "cyan",
        },
    }
    FORMAT = (
        FORMAT
        .replace("<white>", COLORS["white"])
        .replace("</white>", COLORS["reset"])
        .replace("<green>", COLORS["green"])
        .replace("</green>", COLORS["reset"])
    )
    LEVEL_FORMATS: dict[str, str] = {}
    for level, settings in LEVEL_SETTINGS.items():
        fmt = FORMAT
        for name, color in settings.items():
            fmt = (
                fmt
                .replace(f"<{name}>", COLORS[color])
                .replace(f"</{name}>", COLORS["reset"])
            )
        LEVEL_FORMATS[level] = fmt


    class TelegrinderLoggingFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  
            if not record.funcName or record.funcName == "<module>":
                record.funcName = "\b"
            frame = next(
                (
                    frame
                    for frame in inspect.stack()
                    if frame.filename == record.pathname
                    and frame.lineno == record.lineno
                ),
                None,
            )
            if frame:
                module = inspect.getmodule(frame.frame)
                record.module = module.__name__ if module else "<module>"
            return logging.Formatter(
                LEVEL_FORMATS.get(record.levelname),
                datefmt="%Y-%m-%d %H:%M:%S",
                style="{",
            ).format(record)


    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self) -> str:
            return self.fmt.format(*self.args, **self.kwargs)

    class TelegrinderLoggingStyleAdapter(logging.LoggerAdapter):
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, *args, **kwargs):
            if self.isEnabledFor(level):
                kwargs.setdefault("stacklevel", 2)
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
    handler.setFormatter(TelegrinderLoggingFormatter())
    logger = logging.getLogger("telegrinder")  # type: ignore
    logger.setLevel(logging.getLevelName(logging_level))  # type: ignore
    logger.addHandler(handler)  # type: ignore
    logger = TelegrinderLoggingStyleAdapter(logger)  # type: ignore


def _set_logger_level(level):
    level = level.upper()
    if logging_module == "logging":
        import logging

        logging.getLogger("telegrinder").setLevel(logging.getLevelName(level))
    elif logging_module == "loguru":
        import loguru  # type: ignore
        
        if handler_id in loguru.logger._core.handlers:  # type: ignore
            loguru.logger._core.handlers[handler_id]._levelno = loguru.logger.level(level).no  # type: ignore


setattr(logger, "set_level", staticmethod(_set_logger_level))  # type: ignore


__all__ = ("json", "logger")
