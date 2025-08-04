import logging
import os
import typing

from choicelib import choice_in_order

from telegrinder.msgspec_utils import json

# pyright: reportMissingImports=none, reportAttributeAccessIssue=none

if typing.TYPE_CHECKING:
    from logging import Handler as LoggingBasicHandler

    from loguru import AsyncHandlerConfig as LoguruAsyncHandlerConfig
    from loguru import BasicHandlerConfig as LoguruBasicHandlerConfig
    from loguru import FileHandlerConfig as LoguruFileHandlerConfig
    from loguru import HandlerConfig as LoguruHandlerConfig
else:
    LoguruAsyncHandlerConfig = LoguruBasicHandlerConfig = LoguruFileHandlerConfig = dict

type _LoggerHandler = LoggingBasicHandler | LoguruHandlerConfig
type _LoggerLevel = typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "EXCEPTION"]


@typing.runtime_checkable
class LoggerModule(typing.Protocol):
    def debug(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def info(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def warning(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def error(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def critical(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def exception(self, __msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    if typing.TYPE_CHECKING:

        def set_level(self, level: _LoggerLevel, /) -> None: ...

        def set_new_handler(self, new_handler: _LoggerHandler, /) -> None: ...


def _remove_handlers(logger: typing.Any, /) -> None:
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)


def _rich_log_record(record: logging.LogRecord, /) -> logging.LogRecord:
    frame = sys._getframe(1)

    while frame:
        if frame.f_code.co_filename == record.pathname and frame.f_lineno == record.lineno:
            if logging_module == "structlog":
                frame = frame.f_back.f_back.f_back  # pyright: ignore[reportOptionalMemberAccess]

            break

        frame = frame.f_back

    if frame is not None:
        record.funcName = frame.f_code.co_name
        record.module = frame.f_globals.get("__name__", "<module>")
        record.lineno = frame.f_lineno

    if not record.funcName or record.funcName == "<module>":
        record.funcName = "\b"

    return record


class _Logger:
    _logger: LoggerModule | None
    _handler_id: int | None

    def __init__(self) -> None:
        self._logger = None
        self._handler_id = None

    def __repr__(self) -> str:
        return "<Logger {}: {}>".format(
            logging_module,
            "(NOT SETUP)" if self._logger is None else repr(self._logger),
        )

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        return None

    def __getattr__(self, __name: str) -> typing.Any:
        if self._logger is None:
            return self
        return getattr(self._logger, __name)

    def _set_logger(self, logger: LoggerModule, /, *, handler_id: int | None = None) -> None:
        self._logger = logger
        self._handler_id = handler_id

    def set_level(self, level: str, /) -> None:
        if self._logger is None:
            return

        level = level.upper()

        if logging_module in ("logging", "structlog"):
            self._logger.setLevel(level)

        if (
            logging_module == "loguru"
            and self._handler_id is not None
            and self._handler_id in self._logger._core.handlers
        ):
            self._logger._core.handlers[self._handler_id]._levelno = self._logger.level(level).no

    def set_new_handler(self, new_handler: typing.Any, /) -> None:
        if self._logger is None:
            return

        if logging_module in ("logging", "structlog"):
            _remove_handlers(self._logger)
            self._logger.addHandler(new_handler)
        elif logging_module == "loguru" and self._handler_id is not None:
            self._logger.remove(self._handler_id)
            self._handler_id = self._logger.configure(handlers=(new_handler,))[0]


logger: LoggerModule = typing.cast("LoggerModule", _Logger())
logging_module = choice_in_order(["structlog", "loguru"], default="logging", do_import=False)
asyncio_module = choice_in_order(["uvloop", "winloop"], default="asyncio", do_import=False)


if logging_module == "structlog":
    import re
    import sys
    import typing
    from contextlib import suppress

    import colorama
    import structlog

    LEVELS_COLORS = dict(
        debug=colorama.Fore.LIGHTBLUE_EX,
        info=colorama.Fore.LIGHTGREEN_EX,
        warning=colorama.Fore.LIGHTYELLOW_EX,
        error=colorama.Fore.LIGHTRED_EX,
        critical=colorama.Fore.LIGHTRED_EX,
    )

    class SLF4JStyleFormatter:
        BRACE_PATTERN = re.compile(r"\{(?:([^}]*?)(?:!([sra]))?)?\}")
        PERCENT_PATTERN = re.compile(r"%(?:\(([^)]+)\))?([sdfrx])")

        def __init__(self, *, remove_positional_args: bool = True, colors: bool = True) -> None:
            self.remove_positional_args = remove_positional_args
            self.colors = colors

        def __call__(
            self,
            logger: typing.Any,
            method_name: str,
            event_dict: dict[str, typing.Any],
        ) -> dict[str, typing.Any]:
            args = event_dict.get("positional_args", ())
            event = event_dict.pop("event", "")
            if not isinstance(event, str):
                return event_dict

            log_level = event_dict.get("level", "debug")
            system_fields = {"level", "logger", "timestamp", "positional_args"}
            kwargs = {k: v for k, v in event_dict.items() if k not in system_fields}
            used_kwargs = set()

            with suppress(TypeError, ValueError, IndexError, KeyError):
                if self.BRACE_PATTERN.search(event):
                    event_dict["event"], used_kwargs = self._format_braces(event, args, kwargs, log_level)
                elif self.PERCENT_PATTERN.search(event):
                    event_dict["event"], used_kwargs = self._format_percent(event, args, kwargs, log_level)
                elif args:
                    event_dict["event"] = self._highlight_values(event, args, log_level)
                else:
                    event_dict["event"] = event

            if self.remove_positional_args:
                if "positional_args" in event_dict:
                    del event_dict["positional_args"]
                for key in used_kwargs:
                    if key in event_dict:
                        del event_dict[key]

            return event_dict

        def _colorize(self, value: typing.Any, log_level: str) -> str:
            return f"{LEVELS_COLORS[log_level]}{value}{colorama.Fore.RESET}" if self.colors else value

        def _format_braces(
            self,
            message: str,
            args: tuple[typing.Any, ...],
            kwargs: dict[str, typing.Any],
            log_level: str,
        ) -> tuple[str, set[str]]:
            result = []
            last_end = 0
            arg_index = 0
            used_kwargs = set()

            for match in self.BRACE_PATTERN.finditer(message):
                result.append(message[last_end : match.start()])

                field_name = match.group(1)
                conversion = match.group(2)

                if field_name:
                    if field_name in kwargs:
                        value = kwargs[field_name]
                        used_kwargs.add(field_name)
                    else:
                        result.append(match.group(0))
                        last_end = match.end()
                        continue
                elif arg_index < len(args):
                    value = args[arg_index]
                    arg_index += 1
                else:
                    result.append(match.group(0))
                    last_end = match.end()
                    continue

                if conversion == "r":
                    formatted_value = repr(value)
                elif conversion == "s":
                    formatted_value = str(value)
                elif conversion == "a":
                    formatted_value = ascii(value)
                else:
                    formatted_value = str(value)

                result.append(self._colorize(formatted_value, log_level))
                last_end = match.end()

            result.append(message[last_end:])
            return "".join(result), used_kwargs

        def _format_percent(
            self,
            message: str,
            args: tuple[typing.Any, ...],
            kwargs: dict[str, typing.Any],
            log_level: str,
        ) -> tuple[str, set[str]]:
            used_kwargs = set[str]()

            try:
                has_named = bool(re.search(r"%\([^)]+\)", message))
                has_positional = bool(re.search(r"%[sdfrx]", message))

                if has_named and not has_positional:
                    formatted = message % kwargs
                    used_kwargs = set(kwargs.keys())
                    for value in kwargs.values():
                        formatted = self._highlight_single_value(formatted, value, log_level)
                elif has_positional and not has_named:
                    formatted = message % args
                    for value in args:
                        formatted = self._highlight_single_value(formatted, value, log_level)
                elif has_named and has_positional:
                    temp_formatted = message

                    for key, value in kwargs.items():
                        placeholder = f"%({key})s"
                        if placeholder in temp_formatted:
                            used_kwargs.add(key)
                            replacement = self._colorize(str(value), log_level)
                            temp_formatted = temp_formatted.replace(placeholder, replacement)

                    if args and "%s" in temp_formatted:
                        temp_formatted = temp_formatted % args
                        for value in args:
                            temp_formatted = self._highlight_single_value(temp_formatted, value, log_level)

                    formatted = temp_formatted
                else:
                    formatted = message

                return formatted, used_kwargs
            except (TypeError, KeyError, ValueError):
                if kwargs:
                    try:
                        formatted = message % kwargs
                        used_kwargs = set(kwargs.keys())
                        for value in kwargs.values():
                            formatted = self._highlight_single_value(formatted, value, log_level)
                        return formatted, used_kwargs
                    except (TypeError, KeyError):
                        pass

                if args:
                    try:
                        formatted = message % args
                        for value in args:
                            formatted = self._highlight_single_value(formatted, value, log_level)
                        return formatted, used_kwargs
                    except (TypeError, ValueError):
                        pass

                return message, used_kwargs

        def _highlight_single_value(
            self,
            message: str,
            value: typing.Any,
            log_level: str,
        ) -> str:
            with suppress(Exception):
                for raw in (str(value), repr(value)):
                    if raw in message:
                        pattern = re.compile(rf"(?<!\w){re.escape(raw)}(?!\w)")
                        message = pattern.sub(lambda m: self._colorize(m.group(0), log_level), message, count=1)
                        break

            return message

        def _highlight_values(
            self,
            full_message: str,
            values: typing.Iterable[typing.Any],
            log_level: str,
        ) -> str:
            for value in values:
                full_message = self._highlight_single_value(full_message, value, log_level)
            return full_message

    class LogLevelColumnFormatter:
        def __call__(self, key: str, value: typing.Any) -> str:
            color = LEVELS_COLORS[value]
            return f"[{color}{value:^12}{colorama.Fore.RESET}]"

    class Filter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record = _rich_log_record(record)
            level_color = LEVELS_COLORS[record.levelname.lower()]
            location = (
                f"{colorama.Fore.LIGHTCYAN_EX}{record.module}{colorama.Fore.RESET}:"
                f"{level_color}{record.funcName}{colorama.Fore.RESET}:"
                f"{colorama.Fore.LIGHTMAGENTA_EX}{record.lineno}{colorama.Fore.RESET} "
            )
            record.location = location
            return True

    def _configure_structlog(level: str, /) -> LoggerModule:
        console_renderer = structlog.dev.ConsoleRenderer(colors=True)

        for column in console_renderer._columns:
            if column.key == "level":
                column.formatter = LogLevelColumnFormatter()
                break

        fmt = (
            f"[{colorama.Fore.LIGHTBLUE_EX}{{name}}{colorama.Style.RESET_ALL}] "
            f"{colorama.Fore.LIGHTWHITE_EX}{{location}}{colorama.Style.RESET_ALL}"
            f"[{colorama.Fore.LIGHTBLACK_EX}{{asctime}}{colorama.Style.RESET_ALL}] "
            f"{colorama.Fore.LIGHTWHITE_EX}~{colorama.Style.RESET_ALL} {{message}}"
        )

        telegrinder_logger = logging.getLogger("telegrinder")
        telegrinder_logger.setLevel(level)
        _remove_handlers(telegrinder_logger)

        handler = logging.StreamHandler(sys.stderr)
        handler.addFilter(Filter())
        handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S", style="{"))
        telegrinder_logger.addHandler(handler)

        return structlog.wrap_logger(
            logger=telegrinder_logger,
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                SLF4JStyleFormatter(colors=True),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                console_renderer,
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            cache_logger_on_first_use=True,
        )


elif logging_module == "logging":
    import inspect
    import sys

    import colorama

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
            record = _rich_log_record(record)
            return logging.Formatter(
                fmt=LEVEL_FORMATS.get(record.levelname),
                datefmt="%Y-%m-%d %H:%M:%S",
                style="{",
            ).format(record)

    class LogMessage:
        def __init__(self, fmt: str, args: typing.Any, kwargs: typing.Any) -> None:
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self) -> str:
            return self.fmt.format(*self.args, **self.kwargs)

    class TelegrinderLoggingStyleAdapter(logging.LoggerAdapter):
        logger: logging.Logger

        def __init__(
            self,
            logger: logging.Logger,
            **extra: typing.Any,
        ) -> None:
            super().__init__(logger, extra=extra)
            self.log_arg_names = frozenset(inspect.getfullargspec(self.logger._log).args[1:])

        def log(self, level: int, msg: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> None:
            if self.isEnabledFor(level):
                msg, args, kwargs = self.proc(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)

        def proc(
            self,
            msg: typing.Any,
            args: tuple[typing.Any, ...],
            kwargs: dict[str, typing.Any],
        ) -> tuple[typing.Any, tuple[typing.Any, ...], dict[str, typing.Any]]:
            kwargs.setdefault("stacklevel", 2)

            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = tuple()

            return msg, args, {name: kwargs[name] for name in self.log_arg_names if name in kwargs}


if asyncio_module == "uvloop":
    import asyncio

    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

elif asyncio_module == "winloop":
    import asyncio

    import winloop

    asyncio.set_event_loop_policy(winloop.EventLoopPolicy())


def setup_logger(*, level: _LoggerLevel | None = None) -> None:
    import sys

    import colorama

    colorama.just_fix_windows_console()
    colorama.init(wrap=False)

    log_level = level or os.getenv("LOGGER_LEVEL", "DEBUG").upper()

    if logging_module in ("logging", "structlog"):
        if logging_module == "logging":
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(TelegrinderLoggingFormatter())
            _logger = logging.getLogger("telegrinder")
            _logger.setLevel(log_level)
            _remove_handlers(_logger)
            _logger.addHandler(handler)
            logger._set_logger(TelegrinderLoggingStyleAdapter(_logger))
        else:
            logger._set_logger(_configure_structlog(log_level))

    if logging_module == "loguru":
        import loguru

        handler_id = loguru.logger.add(
            sink=sys.stderr,
            level=log_level,
            enqueue=True,
            colorize=True,
            format=(
                "<level>{level: <8}</level> | "
                "<lg>{time:YYYY-MM-DD HH:mm:ss}</lg> | "
                "<le>{name}</le>:<le>{function}</le>:"
                "<le>{line}</le> > <lw>{message}</lw>"
            ),
            filter=lambda record: record["extra"].get("telegrinder", False) is True,
        )
        telegrinder_logger = loguru.logger.bind(telegrinder=True)
        telegrinder_logger._core.handlers = {handler_id: telegrinder_logger._core.handlers[handler_id]}
        logger._set_logger(telegrinder_logger, handler_id=handler_id)


__all__ = (
    "LoggerModule",
    "LoguruAsyncHandlerConfig",
    "LoguruBasicHandlerConfig",
    "LoguruFileHandlerConfig",
    "json",
    "logger",
    "setup_logger",
)
