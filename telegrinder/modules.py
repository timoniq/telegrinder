import os
import typing

from choicelib import choice_in_order

from telegrinder.msgspec_utils import json


@typing.runtime_checkable
class LoggerModule(typing.Protocol):
    def debug(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    def info(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    def warning(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    def error(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    def critical(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    def exception(self, __msg: object, *args: object, **kwargs: object) -> None: ...

    if typing.TYPE_CHECKING:

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
            /,
        ) -> None: ...


logger: LoggerModule
logging_level = os.getenv("LOGGER_LEVEL", default="DEBUG").upper()
logging_module = choice_in_order(["loguru"], default="logging", do_import=False)
asyncio_module = choice_in_order(["uvloop", "winloop"], default="asyncio", do_import=False)

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

    import termcolor

    LOG_FORMAT = (
        termcolor.colored(text=" | ", color="white").join(
            fmt
            for fmt in (
                "{name}",
                "{levelname}",
                "{asctime}",
                "{module}:{funcName}:{lineno}",
            )
        )
        + " {arrow}".format(arrow=termcolor.colored(text=">", color="white"))
        + " {message}"
    )

    LEVEL_FORMAT_SETTINGS = dict(
        DEBUG=dict(
            levelname="light_blue",
            module="blue",
            funcName="blue",
            lineno="light_yellow",
            message="light_blue",
        ),
        INFO=dict(
            levelname="cyan",
            module="light_cyan",
            funcName="light_cyan",
            lineno="light_yellow",
            message="light_green",
        ),
        WARNING=dict(
            levelname="light_yellow",
            module="light_magenta",
            funcName="light_magenta",
            lineno="light_blue",
            message="light_yellow",
        ),
        ERROR=dict(
            levelname="red",
            module="light_yellow",
            funcName="light_yellow",
            lineno="light_blue",
            message="light_red",
        ),
        CRITICAL=dict(
            levelname="magenta",
            module="light_red",
            funcName="light_red",
            lineno="light_yellow",
            message="magenta",
        ),
    )
    NAME_FORMAT = termcolor.colored(text="{name: <4}", color="white")
    ASCTIME_FORMAT = termcolor.colored(text="{asctime}", color="light_green")

    LEVEL_FORMATS = {
        level: LOG_FORMAT.format(
            name=NAME_FORMAT,
            levelname=termcolor.colored(text="{levelname: <8}", color=format_settings.pop("levelname")),
            asctime=ASCTIME_FORMAT,
            **{fmt: termcolor.colored(text="{%s}" % fmt, color=color) for fmt, color in format_settings.items()},
        )
        for level, format_settings in LEVEL_FORMAT_SETTINGS.items()
    }

    class TelegrinderLoggingFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            if not record.funcName or record.funcName == "<module>":
                record.funcName = "\b"

            frame = sys._getframe(1)
            while frame:
                if frame.f_code.co_filename == record.pathname and frame.f_lineno == record.lineno:
                    break

                frame = frame.f_back

            if frame is not None:
                record.module = frame.f_globals.get("__name__", "<module>")

            return logging.Formatter(
                LEVEL_FORMATS.get(record.levelname),
                datefmt="%Y-%m-%d %H:%M:%S",
                style="{",
            ).format(record)

    class LogMessage:
        def __init__(self, fmt: typing.Any, args: typing.Any, kwargs: typing.Any) -> None:
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self) -> str:
            return self.fmt.format(*self.args, **self.kwargs)

    class TelegrinderLoggingStyleAdapter(logging.LoggerAdapter):
        def __init__(
            self,
            logger: LoggerModule,
            extra: dict[str, typing.Any] | None = None,
        ) -> None:
            super().__init__(logger, extra or {})
            self.log_arg_names = frozenset(inspect.getfullargspec(self.logger._log).args[1:])

        def log(self, level: int, msg: object, *args: typing.Any, **kwargs: typing.Any) -> None:
            if self.isEnabledFor(level):
                kwargs.setdefault("stacklevel", 2)
                msg, args, kwargs = self.proc(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)  # type: ignore

        def proc(
            self,
            msg: typing.Any,
            args: tuple[typing.Any, ...],
            kwargs: dict[str, typing.Any],
        ) -> tuple[LogMessage | typing.Any, tuple[typing.Any, ...], dict[str, typing.Any]]:
            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = tuple()
            return msg, args, {name: kwargs[name] for name in self.log_arg_names if name in kwargs}

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(TelegrinderLoggingFormatter())
    logger = logging.getLogger("telegrinder")  # type: ignore
    logger.setLevel(logging_level)  # type: ignore
    logger.addHandler(handler)  # type: ignore
    logger = TelegrinderLoggingStyleAdapter(logger)  # type: ignore

if asyncio_module == "uvloop":
    import asyncio

    import uvloop  # type: ignore

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # type: ignore

if asyncio_module == "winloop":
    import asyncio

    import winloop  # type: ignore

    asyncio.set_event_loop_policy(winloop.EventLoopPolicy())  # type: ignore


def _set_logger_level(level, /):
    level = level.upper()
    if logging_module == "logging":
        import logging

        logging.getLogger("telegrinder").setLevel(level)
    elif logging_module == "loguru":
        import loguru  # type: ignore

        if handler_id in loguru.logger._core.handlers:  # type: ignore
            loguru.logger._core.handlers[handler_id]._levelno = loguru.logger.level(level).no  # type: ignore


setattr(logger, "set_level", staticmethod(_set_logger_level))  # type: ignore


__all__ = ("LoggerModule", "json", "logger")
