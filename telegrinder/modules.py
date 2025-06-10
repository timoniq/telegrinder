import os
import typing

from choicelib import choice_in_order

from telegrinder.msgspec_utils import json

if typing.TYPE_CHECKING:
    from logging import Handler as LoggingBasicHandler

    from loguru import AsyncHandlerConfig as LoguruAsyncHandlerConfig  # type: ignore
    from loguru import BasicHandlerConfig as LoguruBasicHandlerConfig  # type: ignore
    from loguru import FileHandlerConfig as LoguruFileHandlerConfig  # type: ignore
    from loguru import HandlerConfig as LoguruHandlerConfig  # type: ignore
else:
    LoguruAsyncHandlerConfig = LoguruBasicHandlerConfig = LoguruFileHandlerConfig = dict

type _LoggerHandler = LoggingBasicHandler | LoguruHandlerConfig


def _remove_handlers(logger: typing.Any, /) -> None:
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)


@typing.runtime_checkable
class LoggerModule(typing.Protocol):
    def debug(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def info(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def warning(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def error(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def critical(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def exception(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

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

        def set_new_handler(self, new_handler: _LoggerHandler, /) -> None: ...


logger: LoggerModule
logging_level = os.getenv("LOGGER_LEVEL", default="DEBUG").upper()
logging_module = choice_in_order(["structlog", "loguru"], default="logging", do_import=False)
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

elif logging_module == "structlog":
    import logging
    import re
    import sys
    import typing
    from contextlib import suppress

    import colorama
    import structlog  # type: ignore

    LEVELS_COLORS = dict(
        debug=colorama.Fore.LIGHTBLUE_EX,
        info=colorama.Fore.LIGHTGREEN_EX,
        warning=colorama.Fore.LIGHTYELLOW_EX,
        error=colorama.Fore.LIGHTRED_EX,
        critical=colorama.Fore.LIGHTRED_EX,
    )

    class SLF4JStyleFormatter:
        TOKENS = frozenset(("{}", "{!s}", "{!r}", "{!a}"))
        TOKENS_PATTERN = re.compile(r"({!r}|{})")

        def __init__(self, *, remove_positional_args: bool = True) -> None:
            self.remove_positional_args = remove_positional_args

        def __call__(
            self,
            logger: typing.Any,
            method_name: str,
            event_dict: dict[str, typing.Any],
        ) -> dict[str, typing.Any]:
            args = event_dict.get("positional_args")
            if not args:
                return event_dict

            event = event_dict.get("event", "")
            if not isinstance(event, str):
                return event_dict

            log_level = event_dict.get("level", "debug")
            with suppress(TypeError, ValueError, IndexError):
                if "{}" in event or "{!r}" in event:
                    event_dict["event"] = self._safe_format_braces(event, args, log_level)
                elif len(args) == 1 and isinstance(args[0], dict):
                    formatted = event % args[0]
                    event_dict["event"] = self._highlight_values(
                        formatted, args[0].values(), log_level, percent_style=True
                    )
                else:
                    formatted = event % args
                    event_dict["event"] = self._highlight_values(formatted, args, log_level, percent_style=True)

            if self.remove_positional_args and "positional_args" in event_dict:
                del event_dict["positional_args"]

            return event_dict

        def _colorize(self, value: typing.Any, log_level: str) -> str:
            return f"{LEVELS_COLORS[log_level]}{value}{colorama.Fore.RESET}"

        def _safe_format_braces(
            self,
            message: str,
            args: tuple[typing.Any, ...],
            log_level: str,
        ) -> str:
            tokens = self.TOKENS_PATTERN.split(message)
            result = []
            arg_index = 0

            for token in tokens:
                if token in self.TOKENS and arg_index < len(args):
                    result.append(
                        self._colorize(
                            str(args[arg_index]) if token != "{!r}" else repr(args[arg_index]),
                            log_level,
                        ),
                    )
                    arg_index += 1
                else:
                    result.append(token)

            return "".join(result)

        def _highlight_values(
            self,
            full_message: str,
            values: typing.Iterable[typing.Any],
            log_level: str,
            percent_style: bool = False,
        ) -> str:
            for v in values:
                with suppress(Exception):
                    raw = repr(v) if percent_style and ("%r" in full_message) else str(v)
                    pattern = re.compile(rf"(?<!%)\b{re.escape(raw)}\b")
                    full_message = pattern.sub(
                        lambda m: self._colorize(m.group(0), log_level), full_message, count=1
                    )

            return full_message

    class LogLevelColumnFormatter:
        def __call__(self, key: str, value: typing.Any) -> str:
            color = LEVELS_COLORS[value]
            return f"[{color}{value:^12}{colorama.Fore.RESET}]"

    class Filter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            level_color = LEVELS_COLORS[record.levelname.lower()]
            location = (
                f"{colorama.Fore.LIGHTCYAN_EX}{record.module}{colorama.Fore.RESET}:"
                f"{level_color}{record.funcName}{colorama.Fore.RESET}:"
                f"{colorama.Fore.LIGHTMAGENTA_EX}{record.lineno}{colorama.Fore.RESET} "
            )
            record.location = location
            return True

    def configure_logging() -> None:
        console_renderer = structlog.dev.ConsoleRenderer(colors=True)

        for column in console_renderer._columns:
            if column.key == "level":
                column.formatter = LogLevelColumnFormatter()
                break

        structlog.configure(  # type: ignore
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                SLF4JStyleFormatter(),  # type: ignore
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                console_renderer,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        fmt = (
            f"[{colorama.Fore.LIGHTBLUE_EX}{{name}}{colorama.Style.RESET_ALL}] "
            f"{colorama.Fore.LIGHTWHITE_EX}{{location}}{colorama.Style.RESET_ALL}"
            f"[{colorama.Fore.LIGHTBLACK_EX}{{asctime}}{colorama.Style.RESET_ALL}] "
            f"{colorama.Fore.LIGHTWHITE_EX}~{colorama.Style.RESET_ALL} {{message}}"
        )

        telegrinder_logger = logging.getLogger("telegrinder")
        telegrinder_logger.setLevel(logging_level)

        handler = logging.StreamHandler(sys.stderr)
        handler.addFilter(Filter())
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S", style="{")
        handler.setFormatter(formatter)
        _remove_handlers(telegrinder_logger)
        telegrinder_logger.addHandler(handler)

    configure_logging()
    logger = structlog.get_logger("telegrinder")  # type: ignore

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

    colorama.just_fix_windows_console()
    colorama.init()

    LOG_FORMAT = (
        "<light_white>{name: <4} |</light_white> <level>{levelname: <8}</level>"
        " <light_white>|</light_white> <light_green>{asctime}</light_green> <light_white>"
        "|</light_white> <level_module>{module}</level_module><light_white>:</light_white>"
        "<func_name>{funcName}</func_name><light_white>:</light_white><lineno>{lineno}</lineno>"
        " <light_white>></light_white> <message>{message}</message>"
    )
    COLORS = dict(
        reset=colorama.Style.RESET_ALL,
        red=colorama.Fore.RED,
        green=colorama.Fore.GREEN,
        blue=colorama.Fore.BLUE,
        white=colorama.Fore.WHITE,
        yellow=colorama.Fore.YELLOW,
        magenta=colorama.Fore.MAGENTA,
        cyan=colorama.Fore.CYAN,
        light_red=colorama.Fore.LIGHTRED_EX,
        light_green=colorama.Fore.LIGHTGREEN_EX,
        light_blue=colorama.Fore.LIGHTBLUE_EX,
        light_white=colorama.Fore.LIGHTWHITE_EX,
        light_yellow=colorama.Fore.LIGHTYELLOW_EX,
        light_magenta=colorama.Fore.LIGHTMAGENTA_EX,
        light_cyan=colorama.Fore.LIGHTCYAN_EX,
    )
    LEVEL_FORMAT_SETTINGS = dict(
        DEBUG=dict(
            level="light_blue",
            level_module="blue",
            func_name="blue",
            lineno="light_yellow",
            message="light_blue",
        ),
        INFO=dict(
            level="cyan",
            level_module="light_cyan",
            func_name="light_cyan",
            lineno="light_yellow",
            message="light_green",
        ),
        WARNING=dict(
            level="light_yellow",
            level_module="light_magenta",
            func_name="light_magenta",
            lineno="light_blue",
            message="light_yellow",
        ),
        ERROR=dict(
            level="red",
            level_module="light_yellow",
            func_name="light_yellow",
            lineno="light_blue",
            message="light_red",
        ),
        CRITICAL=dict(
            level="magenta",
            level_module="light_red",
            func_name="light_red",
            lineno="light_yellow",
            message="light_magenta",
        ),
    )
    LOG_FORMAT = (
        LOG_FORMAT.replace("<light_white>", COLORS["light_white"])
        .replace("</light_white>", COLORS["reset"])
        .replace("<light_green>", COLORS["light_green"])
        .replace("</light_green>", COLORS["reset"])
    )
    LEVEL_FORMATS = dict[str, str]()

    for level, settings in LEVEL_FORMAT_SETTINGS.items():
        fmt = LOG_FORMAT

        for name, color in settings.items():
            fmt = fmt.replace(f"<{name}>", COLORS[color]).replace(f"</{name}>", COLORS["reset"])

        LEVEL_FORMATS[level] = fmt

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
                fmt=LEVEL_FORMATS.get(record.levelname),
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
            logger: logging.Logger,
            **extra: typing.Any,
        ) -> None:
            super().__init__(logger, extra=extra)
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
    _remove_handlers(logger)
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


def _set_logger_level(level: str, /) -> None:
    level = level.upper()
    if logging_module in ("logging", "structlog"):
        import logging

        logging.getLogger("telegrinder").setLevel(level)
    elif logging_module == "loguru":
        import loguru  # type: ignore

        if handler_id in loguru.logger._core.handlers:  # type: ignore
            loguru.logger._core.handlers[handler_id]._levelno = loguru.logger.level(level).no  # type: ignore


def _set_logger_handler(new_handler: typing.Any, /):
    if logging_module in ("logging", "structlog"):
        import logging

        telegrinder_logger = logging.getLogger("telegrinder")
        _remove_handlers(telegrinder_logger)
        telegrinder_logger.addHandler(new_handler)
    elif logging_module == "loguru":
        import loguru  # type: ignore

        global handler_id  # type: ignore
        loguru.logger.remove(handler_id)  # type: ignore
        handler_id = loguru.logger.configure(handlers=(new_handler,))[0]  # type: ignore


setattr(logger, "set_level", staticmethod(_set_logger_level))
setattr(logger, "set_new_handler", staticmethod(_set_logger_handler))


__all__ = (
    "LoggerModule",
    "LoguruAsyncHandlerConfig",
    "LoguruBasicHandlerConfig",
    "LoguruFileHandlerConfig",
    "json",
    "logger",
)
