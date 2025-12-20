# pyright: reportMissingImports=none, reportAttributeAccessIssue=none, reportMissingModuleSource=none

from __future__ import annotations

import asyncio
import contextvars
import dataclasses
import logging
import os
import re
import sys
import traceback
import types
import typing
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, WatchedFileHandler

from choicelib import choice_in_order

IS_WIN: typing.Final = sys.platform == "win32"

try:
    if IS_WIN:
        import colorama

        colorama.just_fix_windows_console()
        colorama.init(wrap=False)
    else:
        colorama = None
except ImportError:
    colorama = None

if typing.TYPE_CHECKING:
    from _typeshed import OptExcInfo
    from loguru import FileHandlerConfig as _LoguruFileHandler
else:

    class _LoguruFileHandler(dict):
        def __new__(cls, *args, **kwargs):
            if logging_module != "loguru":
                raise ModuleNotFoundError("FileHandlerConfig uses for loguru.") from None

            return super().__new__(cls)


type _LoggerLevel = typing.Literal["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL", "EXCEPTION"]
type _Sink = typing.TextIO | typing.Any

_LoggingFileHandler = RotatingFileHandler | TimedRotatingFileHandler | WatchedFileHandler | logging.FileHandler

_DEFAULT_COLORIZE: typing.Final = not IS_WIN or colorama is not None


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BLACK = "\033[30m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_WHITE = "\033[97m"
    LIGHT_BLACK = "\033[90m"


DEFAULT_LOGGING_FORMAT = (
    ("{name: <4} | {levelname: <8} | {asctime} | {module}:{funcName}:{lineno} > {message}")
    if IS_WIN and colorama is None
    else (
        "<light_white>{name: <4} |</light_white> <level>{levelname: <8}</level>"
        " <light_white>|</light_white> <light_green>{asctime}</light_green> <light_white>"
        "|</light_white> <level_module>{module}</level_module><light_white>:</light_white>"
        "<func_name>{funcName}</func_name><light_white>:</light_white><lineno>{lineno}</lineno>"
        " <light_white>></light_white> <message>{message}</message>"
    )
)
DEFAULT_STRUCTLOG_FORMAT = (
    "[<light_blue>{name}</light_blue>] {location} "
    "[<light_black>{asctime}</light_black>] "
    "<light_white>~</light_white> {message}"
)
DEFAULT_LOGURU_FORMAT = (
    "telegrinder | <level>{level: <8}</level> | "
    "<lg>{time:YYYY-MM-DD HH:mm:ss}</lg> | "
    "<le>{name}</le>:<le>{function}</le>:"
    "<le>{line}</le> > <lw>{message}</lw>"
)

CALL_STACK_CONTEXT = contextvars.ContextVar[tuple[types.FrameType, "OptExcInfo"]]("_call_stack")

if not IS_WIN:
    COLORS = dict(
        reset=Colors.RESET,
        red=Colors.RED,
        green=Colors.GREEN,
        blue=Colors.BLUE,
        white=Colors.WHITE,
        yellow=Colors.YELLOW,
        magenta=Colors.MAGENTA,
        cyan=Colors.CYAN,
        black=Colors.BLACK,
        light_red=Colors.LIGHT_RED,
        light_green=Colors.LIGHT_GREEN,
        light_blue=Colors.LIGHT_BLUE,
        light_white=Colors.LIGHT_WHITE,
        light_yellow=Colors.LIGHT_YELLOW,
        light_magenta=Colors.LIGHT_MAGENTA,
        light_cyan=Colors.LIGHT_CYAN,
        light_black=Colors.LIGHT_BLACK,
    )
else:
    COLORS = (
        dict(
            reset=colorama.Style.RESET_ALL,
            red=colorama.Fore.RED,
            green=colorama.Fore.GREEN,
            blue=colorama.Fore.BLUE,
            white=colorama.Fore.WHITE,
            yellow=colorama.Fore.YELLOW,
            magenta=colorama.Fore.MAGENTA,
            cyan=colorama.Fore.CYAN,
            black=colorama.Fore.BLACK,
            light_red=colorama.Fore.LIGHTRED_EX,
            light_green=colorama.Fore.LIGHTGREEN_EX,
            light_blue=colorama.Fore.LIGHTBLUE_EX,
            light_white=colorama.Fore.LIGHTWHITE_EX,
            light_yellow=colorama.Fore.LIGHTYELLOW_EX,
            light_magenta=colorama.Fore.LIGHTMAGENTA_EX,
            light_cyan=colorama.Fore.LIGHTCYAN_EX,
            light_black=colorama.Fore.LIGHTBLACK_EX,
        )
        if colorama is not None
        else None
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
_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class LoggerModule(typing.Protocol):
    logger: typing.Any

    def set_logger(self, __logger: typing.Any, __logging_module: str) -> None: ...

    def debug(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def info(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def warning(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def success(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def error(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def critical(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def exception(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def adebug(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def ainfo(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def awarning(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def asuccess(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def aerror(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def acritical(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def aexception(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...


class LoggingFormatter(logging.Formatter):
    def __init__(self, format: str, colorize: bool, /) -> None:
        self.level_formats = _get_level_format(format, colorize)
        self.colorize = colorize
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        if logging_module == "logging":
            record = _rich_log_record(record)

        message = logging.Formatter(
            fmt=self.level_formats.get(record.levelname),
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        ).format(record)

        if not self.colorize:
            message = _remove_ansi_colors(message)

        return message


def _remove_handlers(logger: typing.Any, /) -> None:
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)


def _get_level_format(format: str, colorize: bool, /) -> dict[str, str]:
    if COLORS is None:
        return {}

    level_formats = {}

    for level, settings in LEVEL_FORMAT_SETTINGS.items():
        fmt = format

        for name, color in COLORS.items():
            fmt = fmt.replace(f"<{name}>", color if colorize else "").replace(
                f"</{name}>", COLORS["reset"] if colorize else ""
            )

        for name, color in settings.items():
            fmt = fmt.replace(f"<{name}>", COLORS[color] if colorize else "").replace(
                f"</{name}>", COLORS["reset"] if colorize else ""
            )

        level_formats[level] = fmt

    return level_formats


def _rich_log_record(record: logging.LogRecord, /) -> logging.LogRecord:
    call_stack, exc_info = CALL_STACK_CONTEXT.get((None, None))
    frame = call_stack or sys._getframe(1)

    if call_stack is None:
        while frame:
            if frame.f_code.co_filename == record.pathname and frame.f_lineno == record.lineno:
                if logging_module == "structlog":
                    frame = frame.f_back.f_back.f_back  # pyright: ignore[reportOptionalMemberAccess]

                break

            frame = frame.f_back

    if record.levelno >= logging.ERROR and record.exc_info is not None:
        if exc_info is not None and any(exc_info):
            record.exc_info = exc_info
        elif logging_module == "structlog":
            record.exc_info = None

    if frame is not None:
        record.funcName = frame.f_code.co_name
        record.module = frame.f_globals.get("__name__", "<module>")
        record.lineno = frame.f_lineno

    if not record.funcName or record.funcName == "<module>":
        record.funcName = "\b"

    return record


def _loguru_filter(record: dict[str, typing.Any]) -> bool:
    if record["extra"].get("telegrinder", False) is not True:
        return False

    frame, exc_info = CALL_STACK_CONTEXT.get((None, None))

    if frame is not None:
        if "file" in record:
            file_name = frame.f_code.co_filename
            record["file"].name = os.path.basename(file_name)
            record["file"].path = file_name

        record["name"] = frame.f_globals.get("__name__", "<module>")
        record["module"] = record["name"].split(".")[-1]
        record["line"] = frame.f_lineno
        record["function"] = frame.f_code.co_name

    if (
        exc_info is not None
        and any(exc_info)
        and record["exception"] is not None
        and not any(record["exception"])
        and record["level"].no >= logger.logger.level("ERROR").no
    ):
        from loguru._recattrs import RecordException  # type: ignore

        record["exception"] = RecordException(exc_info[0], exc_info[1], exc_info[2])  # type: ignore

    return True


def _remove_ansi_colors(text: str) -> str:
    return _ANSI_ESCAPE.sub("", text)


class _json:  # noqa: N801
    def __getattr__(self, __name: str) -> typing.Any:
        from telegrinder.msgspec_utils import json

        return getattr(json, __name)

    def __repr__(self) -> str:
        return "<module 'telegrinder.msgspec_utils.json'>"


class _LoggerProxy:
    def __init__(self) -> None:
        self.logger = None
        self.module_logger = None

    def __repr__(self) -> str:
        return "<LoggerProxy {}: {}>".format(
            self.logging_module,
            "(NOT SETUP)" if self.logger is None else repr(self.logger),
        )

    def __await__(self) -> typing.Generator[typing.Any, typing.Any, typing.Any]:
        return iter(())  # type: ignore

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        return self

    def __getattr__(self, __name: str) -> typing.Any:
        if self.logger is None:
            if __name == "exception" and (exception := sys.exception()) is not None:
                traceback.print_exception(exception, chain=True, colorize=True)  # type: ignore

            return self

        if __name in LoggerModule.__dict__:
            is_async = __name.startswith("a")
            method_name = __name.removeprefix("a") if is_async else __name
            method_name = "info" if method_name == "success" and self.logging_module != "loguru" else method_name
            level_name = __name.removeprefix("a").upper()
            level_name = (
                "INFO"
                if level_name == "SUCCESS" and self.logging_module != "loguru"
                else "ERROR"
                if level_name == "EXCEPTION"
                else level_name
            )
            level = (
                logging._nameToLevel.get(level_name, logging.NOTSET) if self.logging_module != "loguru" else level_name
            )
            level_is_enabled = hasattr(self.logger, "isEnabledFor") and self.logger.isEnabledFor(level)

            if is_async:
                meth = getattr(self.logger, method_name)
                method = (
                    self if not level_is_enabled else lambda *args, **kwargs: self._async_log(meth, *args, **kwargs)
                )
            else:
                method = getattr(self.logger, method_name) if level_is_enabled else self

            return method

        return getattr(self.logger, __name)

    async def _async_log(
        self,
        method: typing.Callable[..., typing.Any],
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        tok = CALL_STACK_CONTEXT.set((sys._getframe(0).f_back, sys.exc_info()))  # type: ignore
        ctx = contextvars.copy_context()

        try:
            await asyncio.get_running_loop().run_in_executor(
                executor=None,
                func=lambda: ctx.run(lambda: method(*args, **kwargs)),
            )
        finally:
            CALL_STACK_CONTEXT.reset(tok)

    def set_logger(self, logger: LoggerModule, logging_module: str) -> None:
        self.logger = logger
        self.logging_module = logging_module


class _LoguruFileHandlerConfig(_LoguruFileHandler):
    pass


@dataclasses.dataclass
class FileHandlerConfig:
    handler: _LoggingFileHandler | _LoguruFileHandlerConfig
    format: str | None = None
    colorize: bool = False

    def __post_init__(self) -> None:
        self.format = (
            os.environ.get("TELEGRINDER_LOGGER_FILE_HANDLER_FORMAT", None)
            or self.format
            or (
                DEFAULT_LOGGING_FORMAT
                if logging_module == "logging"
                else DEFAULT_STRUCTLOG_FORMAT
                if logging_module == "structlog"
                else DEFAULT_LOGURU_FORMAT
            )
        )
        self.colorize = (
            os.environ.get("TELEGRINDER_LOGGER_FILE_HANDLER_COLORIZE", "0").lower() in ("1", "true", "on")
            or self.colorize
        )

    @classmethod
    def from_logging(
        cls,
        handler: _LoggingFileHandler,
        format: str | None = None,
        colorize: bool = False,
    ) -> typing.Self:
        return cls(handler, format, colorize)

    @classmethod
    def from_loguru(
        cls,
        **kwargs: typing.Unpack[_LoguruFileHandlerConfig],  # type: ignore
    ) -> typing.Self:
        return cls(kwargs)  # type: ignore


logger: LoggerModule = typing.cast("LoggerModule", _LoggerProxy())
logging_module = (
    choice_in_order(["structlog", "loguru"], default="logging", do_import=False)
    if (_module := os.environ.get("TELEGRINDER_LOGGER_MODULE", None)) is None
    else _module
)
asyncio_module = choice_in_order(["uvloop", "winloop"], default="asyncio", do_import=False)


if logging_module == "structlog":
    import re
    import sys
    import typing
    from contextlib import suppress

    import structlog

    _LEVELS_COLORS = (
        dict(
            debug=COLORS["light_blue"],
            info=COLORS["light_green"],
            warning=COLORS["light_yellow"],
            error=COLORS["light_red"],
            critical=COLORS["light_red"],
        )
        if COLORS is not None
        else None
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
            event_dict: typing.MutableMapping[str, typing.Any],
        ) -> typing.MutableMapping[str, typing.Any]:
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
            if _LEVELS_COLORS is None:
                return value

            return f"{_LEVELS_COLORS[log_level]}{value}{Colors.RESET}" if self.colors else value

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
        def __init__(self, colorize: bool) -> None:
            self.colorize = colorize

        def __call__(self, key: str, value: typing.Any) -> str:
            if self.colorize and _LEVELS_COLORS is not None:
                color = _LEVELS_COLORS[value]
                return f"[{color}{value:^12}{Colors.RESET}]"

            return f"[{value:^12}]"

    class Filter(logging.Filter):
        def __init__(self, colorize: bool) -> None:
            self.colorize = colorize
            super().__init__()

        def filter(self, record: logging.LogRecord) -> bool:
            record = _rich_log_record(record)

            if self.colorize and _LEVELS_COLORS is not None:
                level_color = _LEVELS_COLORS[record.levelname.lower()]
                location = (
                    f"{Colors.LIGHT_CYAN}{record.module}{Colors.RESET}:"
                    f"{level_color}{record.funcName}{Colors.RESET}:"
                    f"{Colors.LIGHT_MAGENTA}{record.lineno}{Colors.RESET} "
                )
            else:
                location = f"{record.module}:{record.funcName}:{record.lineno} "

            record.location = location
            return True

    def _configure_structlog(
        level: str,
        format: str | None = None,
        colorize: bool = True,
        console_sink: _Sink | None = None,
        file: FileHandlerConfig | None = None,
        /,
    ) -> None:
        if all((colorize is True, COLORS is None, IS_WIN)):
            raise RuntimeError("colorama is required to colorize logging output on Windows.")

        console_renderer = structlog.dev.ConsoleRenderer(colors=True)

        for column in console_renderer._columns:
            if column.key == "level":
                column.formatter = LogLevelColumnFormatter(colorize)
                break

        telegrinder_logger = logging.getLogger("telegrinder")
        telegrinder_logger.setLevel(level)
        _remove_handlers(telegrinder_logger)

        if console_sink is not None:
            console_handler = logging.StreamHandler(console_sink)
            console_handler.setFormatter(LoggingFormatter(format or DEFAULT_STRUCTLOG_FORMAT, colorize))
            console_handler.addFilter(Filter(colorize))
            telegrinder_logger.addHandler(console_handler)

        if file is not None and isinstance(file.handler, _LoggingFileHandler):
            if file.handler.formatter is None:
                file.handler.setFormatter(LoggingFormatter(file.format, file.colorize))  # type: ignore

            file.handler.addFilter(Filter(file.colorize))
            telegrinder_logger.addHandler(file.handler)

        struct_logger = structlog.wrap_logger(
            logger=telegrinder_logger,
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                SLF4JStyleFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                console_renderer,
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            cache_logger_on_first_use=True,
        )
        logger.set_logger(struct_logger, "structlog")


elif logging_module == "loguru":

    def _configure_loguru(
        level: str,
        format: str | None = None,
        colorize: bool = True,
        console_sink: _Sink | None = None,
        file: FileHandlerConfig | None = None,
        /,
    ) -> None:
        import atexit

        from loguru._logger import Core, Logger

        loguru_logger = Logger(
            core=Core(),
            exception=None,
            depth=0,
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra=dict(telegrinder=True),
        )

        def is_enabled_for(level: str) -> bool:
            try:
                lno = loguru_logger.level(level).no
            except ValueError:
                return False

            return any(lno >= x.levelno for x in loguru_logger._core.handlers.values())

        loguru_logger.isEnabledFor = is_enabled_for
        handlers = []

        if console_sink is not None:
            handlers.append(
                dict(
                    sink=console_sink,
                    level=level,
                    enqueue=True,
                    colorize=colorize,
                    format=format or DEFAULT_LOGURU_FORMAT,
                    filter=_loguru_filter,
                ),
            )

        if file is not None and isinstance(file.handler, dict):  # type: ignore
            file.handler.setdefault("format", file.format or DEFAULT_LOGURU_FORMAT)
            file.handler.setdefault("colorize", file.colorize)
            handlers.append(file.handler)

        if handlers:
            handlers_ids = loguru_logger.configure(handlers=handlers)

            @atexit.register
            def _() -> None:
                for handler_id in handlers_ids:
                    loguru_logger.remove(handler_id)

        logger.set_logger(loguru_logger, "loguru")


elif logging_module == "logging":
    import inspect
    import sys

    class LogMessage:
        def __init__(self, fmt: str, args: typing.Any, kwargs: typing.Any) -> None:
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self) -> str:
            return self.fmt.format(*self.args, **self.kwargs)

    class LoggingStyleAdapter(logging.LoggerAdapter):
        logger: logging.Logger

        def __init__(
            self,
            logger: logging.Logger,
            **extra: typing.Any,
        ) -> None:
            super().__init__(logger, extra=extra or None)
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

    def _configure_logging(
        level: str,
        format: str | None = None,
        colorize: bool = True,
        console_sink: _Sink | None = None,
        file: FileHandlerConfig | None = None,
        /,
    ) -> None:
        if all((colorize is True, COLORS is None, IS_WIN)):
            raise RuntimeError("colorama is required to colorize logging output on Windows.")

        _logger = logging.getLogger("telegrinder")
        _logger.setLevel(level)
        _remove_handlers(_logger)

        if console_sink is not None:
            console_handler = logging.StreamHandler(console_sink)
            console_handler.setFormatter(LoggingFormatter(format or DEFAULT_LOGGING_FORMAT, colorize))
            _logger.addHandler(console_handler)

        if file is not None and isinstance(file.handler, _LoggingFileHandler):
            if file.handler.formatter is None:
                file.handler.setFormatter(LoggingFormatter(file.format, file.colorize))  # type: ignore

            _logger.addHandler(file.handler)

        logger.set_logger(LoggingStyleAdapter(logger=_logger), "logging")


if asyncio_module in ("uvloop", "winloop"):
    import asyncio

    asyncio.set_event_loop_policy(policy=__import__(name=asyncio_module).EventLoopPolicy())


def setup_logger(
    *,
    console_sink: _Sink | None = sys.stderr,
    level: _LoggerLevel | None = None,
    format: str | None = None,
    colorize: bool = _DEFAULT_COLORIZE,
    file: FileHandlerConfig | None = None,
) -> LoggerModule:
    if logger.logger is not None:
        return logger

    args: tuple[typing.Any, ...] = (
        (os.environ.get("TELEGRINDER_LOGGER_LEVEL", None) or level or "debug").upper(),
        os.environ.get("TELEGRINDER_LOGGER_FORMAT", None) or format,
        os.environ.get("TELEGRINDER_LOGGER_COLORIZE", "0").lower() in ("1", "true", "on") or colorize,
        console_sink,
        file,
    )

    match logging_module:
        case "logging":
            _configure_logging(*args)
        case "loguru":
            _configure_loguru(*args)
        case "structlog":
            _configure_structlog(*args)

    return logger


if typing.TYPE_CHECKING:
    from telegrinder.msgspec_utils import json
else:
    json = _json()


__all__ = ("FileHandlerConfig", "json", "logger", "setup_logger")
