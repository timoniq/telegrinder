# pyright: reportMissingImports=none, reportAttributeAccessIssue=none, reportMissingModuleSource=none

import asyncio
import contextlib
import contextvars
import inspect
import logging
import os
import pathlib
import re
import shlex
import sys
import traceback
import types
import typing
from annotationlib import type_repr
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, WatchedFileHandler

import betterconf
from choicelib import choice_in_order
from kungfu.library.monad.option import NOTHING, Option, Some

if typing.TYPE_CHECKING:
    from _typeshed import OptExcInfo
    from loguru import FileHandlerConfig as _LoguruFileHandler
else:

    class _LoguruFileHandler(dict):
        def __new__(cls, *args, **kwargs):
            if logging_module != "loguru":
                raise ModuleNotFoundError("FileHandlerConfig uses for loguru.") from None

            return super().__new__(cls)


type LoggerModule = typing.Literal["logging", "loguru", "structlog"]
type Sink = typing.TextIO | typing.Any
type LoggerLevel = typing.Literal["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL", "EXCEPTION"]

_LoggingFileHandler = RotatingFileHandler | TimedRotatingFileHandler | WatchedFileHandler | logging.FileHandler


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


LOGGER_MODULE: typing.Final = typing.cast(
    "LoggerModule",
    choice_in_order(["structlog", "loguru"], default="logging", do_import=False),
)
DEFAULT_LOGGING_FORMAT: typing.Final = (
    "<light_white>{name: <4} |</light_white> <level>{levelname: <8}</level>"
    " <light_white>|</light_white> <light_green>{asctime}</light_green> <light_white>"
    "|</light_white> <level_module>{module}</level_module><light_white>:</light_white>"
    "<func_name>{funcName}</func_name><light_white>:</light_white><lineno>{lineno}</lineno>"
    " <light_white>></light_white> <message>{message}</message>"
)
DEFAULT_STRUCTLOG_FORMAT: typing.Final = (
    "[<light_blue>{name}</light_blue>] {location} "
    "[<light_black>{asctime}</light_black>] "
    "<light_white>~</light_white> {message}"
)
DEFAULT_LOGURU_FORMAT: typing.Final = (
    "telegrinder | <level>{level: <8}</level> | "
    "<lg>{time:YYYY-MM-DD HH:mm:ss}</lg> | "
    "<le>{name}</le>:<le>{function}</le>:"
    "<le>{line}</le> > <lw>{message}</lw>"
)

CALL_STACK_CONTEXT: typing.Final = contextvars.ContextVar[tuple[types.FrameType, "OptExcInfo"]]("_call_stack")
LOG_SCOPE: typing.Final = contextvars.ContextVar[str]("_log_scope", default="")

COLORS: typing.Final = dict(
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
LEVEL_FORMAT_SETTINGS: typing.Final = dict(
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
VARIABLE_NAME_PATTERN: typing.Final = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
ASSIGNMENT_OPERATOR: typing.Final = "="
LOGGER_LEVELS: typing.Final = ("DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL", "EXCEPTION")
LOGGER_MODULES: typing.Final = ("logging", "loguru", "structlog")
_NODEFAULT: typing.Final = typing.cast("typing.Any", object())
_LOAD_ENV_FILE = False
_ENV_FILE_NAME = ".env"
_ENV_FILE_PATH: pathlib.Path | None = None
_ANSI_ESCAPE: typing.Final = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def _find_env_file() -> Option[pathlib.Path]:
    caller_frame = sys._getframe()

    while caller_frame:
        if caller_frame.f_back is None:
            break

        caller_frame = caller_frame.f_back

    caller_dir = os.path.dirname(caller_frame.f_code.co_filename)
    start_dir = sys.path[0]

    # Handle empty paths (can happen on Windows in certain launch conditions)
    if not caller_dir or not start_dir:
        search_path = caller_dir or start_dir or "."
    else:
        try:
            search_path = os.path.relpath(caller_dir, start_dir)
        except ValueError:
            search_path = caller_dir

    for root, _, files in os.walk(search_path):
        if _ENV_FILE_NAME in files:
            return Some(pathlib.Path(root) / _ENV_FILE_NAME)

    return NOTHING


@contextlib.contextmanager
def log_scope(
    ident: str | typing.Callable[..., str],
    /,
    *args: typing.Any,
    **kwargs: typing.Any,
) -> typing.Iterator[None]:
    """Context manager to set a log scope for the current async task.

    >>> with log_scope("{handlers_folder} → {view!r}", handlers_folder="handlers", view=view):
    ...     await logger.adebug("hello, admin!")  # [handlers → MessageView] hello, admin!
    """

    if logger.logger is not None:
        current = LOG_SCOPE.get("")
        ident = ident.format(*args, **kwargs) if isinstance(ident, str) else ident(*args, **kwargs)
        token = LOG_SCOPE.set(" → ".join((current, ident)) if current else ident)

        try:
            yield
        finally:
            LOG_SCOPE.reset(token)
    else:
        yield


@typing.overload
def take_env(var_name: str, /) -> str: ...


@typing.overload
def take_env[T](var_name: str, var_type: type[T], /) -> T: ...


@typing.overload
def take_env[T](var_name: str, var_type: type[T], /, *, default: T) -> T: ...


def take_env[T](
    name: str,
    var_type: type[T] = str,
    /,
    *,
    default: T = _NODEFAULT,
) -> T:
    try:
        value = DOTENV.get(name)
    except betterconf.VariableNotFoundError:
        if default is _NODEFAULT:
            raise
        return default

    if var_type is str:
        return value  # type: ignore

    if var_type not in CASTERS:
        raise NotImplementedError(f"Caster for type `{type_repr(var_type)}` is not implemented.")

    return CASTERS[var_type].cast(value)


class _LoggerLevelCaster(betterconf.AbstractCaster):
    def cast(self, value: str) -> LoggerLevel:
        if value not in LOGGER_LEVELS:
            raise betterconf.ImpossibleToCastError(value, self)
        return value


class _LoggerModuleCaster(betterconf.AbstractCaster):
    def cast(self, value: str) -> LoggerModule:
        if value not in LOGGER_MODULES:
            raise betterconf.ImpossibleToCastError(value, self)
        return value


class _DotenvProvider(betterconf.AbstractProvider):
    __slots__ = ("env_file", "loaded")

    env_file: pathlib.Path | None
    loaded: bool

    def __init__(self) -> None:
        self.env_file = None
        self.loaded = False

    def load(self) -> None:
        if self.loaded:
            return

        self.loaded = True
        self.env_file = _ENV_FILE_PATH if _ENV_FILE_PATH is not None else _find_env_file().unwrap_or_none()

        if self.env_file is None:
            return

        variables: dict[str, str] = {}

        for line in self.env_file.read_text().splitlines():
            match tuple(shlex.shlex(instream=line, posix=True)):
                case (var_name, operator, *tokens) if (
                    tokens and operator == ASSIGNMENT_OPERATOR and VARIABLE_NAME_PATTERN.match(var_name)
                ):
                    variables[var_name] = "".join(tokens).replace(r"\n", "\n").replace(r"\t", "\t")
                case _:
                    continue

        os.environ.update(variables)

    def get(self, name: str) -> str:
        if not self.loaded and _LOAD_ENV_FILE is True:
            self.load()
        return ENV.get(name)


DOTENV: typing.Final = _DotenvProvider()
ENV: typing.Final = betterconf.EnvironmentProvider()
CASTERS: typing.Final[dict[type[typing.Any], betterconf.AbstractCaster]] = {
    LoggerLevel: (to_logger_level := _LoggerLevelCaster()),  # type: ignore
    **betterconf.caster.BUILTIN_CASTERS,
}


@betterconf.betterconf(prefix="TELEGRINDER_LOGGER", provider=DOTENV)
class LoggerConfig:
    MODULE: typing.Literal["logging", "loguru", "structlog"] = betterconf.field(
        default=LOGGER_MODULE,
        caster=_LoggerModuleCaster(),
    )
    LEVEL: LoggerLevel = betterconf.field(
        default="DEBUG",
        caster=to_logger_level,
    )
    FORMAT: str | None = betterconf.constant_field(None)
    COLORIZE: bool = betterconf.field(
        default=True,
        caster=betterconf.caster.to_bool,
    )
    FILE_HANDLER_FORMAT: str | None = betterconf.constant_field(None)
    FILE_HANDLER_COLORIZE: bool = betterconf.field(
        default=False,
        caster=betterconf.caster.to_bool,
    )


def _is_async_logger(logger: typing.Any, /) -> bool:
    return all(hasattr(logger, attr) for attr in AnyAsyncLogger.__protocol_attrs__)


class AnyLogger(typing.Protocol):
    def debug(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def info(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def warning(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def error(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def critical(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    def exception(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...


class AnyAsyncLogger(typing.Protocol):
    async def adebug(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def ainfo(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def awarning(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def aerror(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def acritical(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...

    async def aexception(self, __msg: str, *args: typing.Any, **kwargs: typing.Any) -> None: ...


class Logger(AnyLogger, AnyAsyncLogger, typing.Protocol):
    def set_logger(self, __logger: AnyLogger) -> None: ...


class WrapperAsyncLogger:
    def __init__(self, logger: Logger, /) -> None:
        self._logger = logger

    def __getattr__(self, __name: str) -> typing.Any:
        if __name in AnyAsyncLogger.__dict__:
            return lambda *args, **kwargs: self._async_log(
                getattr(self._logger, __name.removeprefix("a")),
                *args,
                **kwargs,
            )

        return super().__getattribute__(__name)

    async def _async_log(
        self,
        method: typing.Callable[..., typing.Any],
        /,
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


class LoggingFormatter(logging.Formatter):
    def __init__(self, format: str, colorize: bool, logger_module: str, /) -> None:
        self.level_formats = _get_level_format(format, colorize)
        self.colorize = colorize
        self.logger_module = logger_module
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        if self.logger_module == "logging":
            record = _rich_log_record(record, self.logger_module)

        message = logging.Formatter(
            fmt=self.level_formats.get(record.levelname),
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        ).format(record)

        if not self.colorize:
            message = _remove_ansi_colors(message)

        return message


class LogMessage:
    def __init__(self, fmt: str, args: typing.Any, kwargs: typing.Any) -> None:
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        message = self.fmt.format(*self.args, **self.kwargs)
        scope = LOG_SCOPE.get("")
        return f"[{scope}] {message}" if scope else message


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


def _remove_handlers(logger: typing.Any, /) -> None:
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)


def _get_level_format(format: str, colorize: bool, /) -> dict[str, str]:
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


def _rich_log_record(record: logging.LogRecord, logger_module: str, /) -> logging.LogRecord:
    call_stack, exc_info = CALL_STACK_CONTEXT.get((None, None))
    frame = call_stack or sys._getframe(1)

    if call_stack is None:
        while frame:
            if frame.f_code.co_filename == record.pathname and frame.f_lineno == record.lineno:
                if logger_module == "structlog":
                    frame = frame.f_back.f_back.f_back  # pyright: ignore[reportOptionalMemberAccess]

                break

            frame = frame.f_back

    if record.levelno >= logging.ERROR and record.exc_info is not None:
        if exc_info is not None and any(exc_info):
            record.exc_info = exc_info
        elif logger_module == "structlog":
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

    scope = LOG_SCOPE.get("")
    if scope:
        record["message"] = f"[{scope}] {record['message']}"

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
        self.logger_module = None

    def __repr__(self) -> str:
        return "<LoggerProxy {}: {}>".format(
            self.logger_module or "unknown",
            "(NOT SETUP)" if self.logger is None else repr(self.logger),
        )

    def __await__(self) -> typing.Generator[typing.Any, typing.Any, typing.Any]:
        return iter(())  # type: ignore

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        return self

    def __getattr__(self, __name: str) -> typing.Any:
        if self.logger is None:
            if __name in ("exception", "aexception") and (exc := sys.exception()) is not None:
                traceback.print_exception(exc, chain=True, file=sys.stderr)

            return self

        if __name in AnyLogger.__dict__ or __name in AnyAsyncLogger.__dict__:
            is_async = __name.startswith("a")

            if self.logging_module is not None:
                level_name = __name.removeprefix("a").upper()
                level_name = (
                    "INFO"
                    if level_name == "SUCCESS" and self.logger_module != "loguru"
                    else "ERROR"
                    if level_name == "EXCEPTION"
                    else level_name
                )
                level = (
                    logging._nameToLevel.get(level_name, logging.NOTSET)
                    if self.logger_module != "loguru"
                    else level_name
                )
                if not hasattr(self.logger, "isEnabledFor") and self.logger.isEnabledFor(level):  # type: ignore
                    return self

            return getattr(self.logger if not is_async else self.async_logger, __name)

        return self

    def set_logger(self, logger: Logger, logger_module: LoggerModule | None = None) -> None:
        self.logger = logger if not isinstance(logger, logging.Logger) else LoggingStyleAdapter(logger)
        self.async_logger = WrapperAsyncLogger(logger) if not _is_async_logger(logger) else logger
        self.logger_module = logger_module


class _SetupLoggerKwargs(typing.TypedDict):
    module: typing.NotRequired[LoggerModule]
    level: typing.NotRequired[LoggerLevel]
    format: typing.NotRequired[str]
    colorize: typing.NotRequired[bool]
    console_sink: typing.NotRequired[Sink | None]
    file: typing.NotRequired[FileHandlerConfig]


class _LoguruFileHandlerConfig(_LoguruFileHandler):
    pass


class FileHandlerConfig:
    handler: _LoggingFileHandler | _LoguruFileHandlerConfig
    format: str
    colorize: bool

    def __init__(
        self,
        handler: _LoggingFileHandler | _LoguruFileHandlerConfig,
        format: str = _NODEFAULT,
        colorize: bool = _NODEFAULT,
        logger_module: str = LOGGER_MODULE,
    ) -> None:
        config = LoggerConfig()
        format = (config.FILE_HANDLER_FORMAT if format is _NODEFAULT else format) or (
            DEFAULT_LOGURU_FORMAT
            if logger_module == "loguru"
            else DEFAULT_STRUCTLOG_FORMAT
            if logger_module == "structlog"
            else DEFAULT_LOGGING_FORMAT
        )
        colorize = config.FILE_HANDLER_COLORIZE if colorize is _NODEFAULT else colorize

        self.handler = handler

        if isinstance(self.handler, dict):
            self.format = self.handler.setdefault("format", format)
            self.colorize = self.handler.setdefault("colorize", colorize)
        else:
            self.format = format
            self.colorize = colorize

            if handler.formatter is None:
                handler.setFormatter(LoggingFormatter(format, colorize, logger_module))

    @classmethod
    def from_logging(
        cls,
        handler: _LoggingFileHandler,
        format: str = _NODEFAULT,
        colorize: bool = _NODEFAULT,
    ) -> typing.Self:
        return cls(handler, format, colorize)

    @classmethod
    def from_loguru(
        cls,
        **kwargs: typing.Unpack[_LoguruFileHandlerConfig],  # type: ignore
    ) -> typing.Self:
        return cls(kwargs)  # type: ignore


logger: Logger = typing.cast("Logger", _LoggerProxy())


def _configure_structlog(
    level: LoggerLevel,
    format: str | None,
    colorize: bool,
    console_sink: Sink | None = None,
    file: FileHandlerConfig | None = None,
    /,
) -> None:
    import re
    from contextlib import suppress

    import structlog

    levels_colors = dict(
        debug=COLORS["light_blue"],
        info=COLORS["light_green"],
        warning=COLORS["light_yellow"],
        error=COLORS["light_red"],
        critical=COLORS["light_red"],
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

            scope = LOG_SCOPE.get("")
            if scope and "event" in event_dict:
                event_dict["event"] = f"[{scope}] {event_dict['event']}"

            return event_dict

        def _colorize(self, value: typing.Any, log_level: str) -> str:
            return f"{levels_colors[log_level]}{value}{Colors.RESET}" if self.colors else value

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
            except TypeError, KeyError, ValueError:
                if kwargs:
                    try:
                        formatted = message % kwargs
                        used_kwargs = set(kwargs.keys())
                        for value in kwargs.values():
                            formatted = self._highlight_single_value(formatted, value, log_level)
                        return formatted, used_kwargs
                    except TypeError, KeyError:
                        pass

                if args:
                    try:
                        formatted = message % args
                        for value in args:
                            formatted = self._highlight_single_value(formatted, value, log_level)
                        return formatted, used_kwargs
                    except TypeError, ValueError:
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
            if self.colorize:
                color = levels_colors[value]
                return f"[{color}{value:^12}{Colors.RESET}]"

            return f"[{value:^12}]"

    class Filter(logging.Filter):
        def __init__(self, colorize: bool) -> None:
            self.colorize = colorize
            super().__init__()

        def filter(self, record: logging.LogRecord) -> bool:
            record = _rich_log_record(record, "structlog")

            if self.colorize:
                level_color = levels_colors[record.levelname.lower()]
                location = (
                    f"{Colors.LIGHT_CYAN}{record.module}{Colors.RESET}:"
                    f"{level_color}{record.funcName}{Colors.RESET}:"
                    f"{Colors.LIGHT_MAGENTA}{record.lineno}{Colors.RESET} "
                )
            else:
                location = f"{record.module}:{record.funcName}:{record.lineno} "

            record.location = location
            return True

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
        console_handler.setFormatter(LoggingFormatter(format or DEFAULT_STRUCTLOG_FORMAT, colorize, "structlog"))
        console_handler.addFilter(Filter(colorize))
        telegrinder_logger.addHandler(console_handler)

    if file is not None and isinstance(file.handler, _LoggingFileHandler):
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
    logger.set_logger(struct_logger, "structlog")  # type: ignore


def _configure_loguru(
    level: LoggerLevel,
    format: str | None,
    colorize: bool,
    console_sink: Sink | None = None,
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

    def is_enabled_for(lvl: str) -> bool:
        try:
            lno = loguru_logger.level(lvl).no
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
        handlers.append(file.handler)

    if handlers:
        handlers_ids = loguru_logger.configure(handlers=handlers)

        @atexit.register
        def _() -> None:
            for handler_id in handlers_ids:
                loguru_logger.remove(handler_id)

    logger.set_logger(loguru_logger, "loguru")  # type: ignore


def _configure_logging(
    level: LoggerLevel,
    format: str | None,
    colorize: bool,
    console_sink: Sink | None = None,
    file: FileHandlerConfig | None = None,
    /,
) -> None:
    _logger = logging.getLogger("telegrinder")
    _logger.setLevel(level)
    _remove_handlers(_logger)

    if console_sink is not None:
        console_handler = logging.StreamHandler(console_sink)
        console_handler.setFormatter(LoggingFormatter(format or DEFAULT_LOGGING_FORMAT, colorize, "logging"))
        _logger.addHandler(console_handler)

    if file is not None and isinstance(file.handler, _LoggingFileHandler):
        _logger.addHandler(file.handler)

    logger.set_logger(LoggingStyleAdapter(logger=_logger), "logging")  # type: ignore


def setup_logger(**setup_kwargs: typing.Unpack[_SetupLoggerKwargs]) -> Logger:
    if logger.logger is not None:
        return logger

    config = LoggerConfig()
    args = (
        setup_kwargs.get("level", config.LEVEL),
        setup_kwargs.get("format", config.FORMAT),
        setup_kwargs.get("colorize", config.COLORIZE),
        setup_kwargs.get("console_sink", sys.stderr),
        setup_kwargs.get("file"),
    )

    match setup_kwargs.get("module", config.MODULE):
        case "logging":
            _configure_logging(*args)
        case "loguru":
            _configure_loguru(*args)
        case "structlog":
            _configure_structlog(*args)
        case _ as value:
            typing.assert_never(value)

    return logger


def configure_dotenv(
    *,
    load_file: bool = _LOAD_ENV_FILE,
    file_name: str | None = _ENV_FILE_PATH,
    file_path: str | pathlib.Path | None = _ENV_FILE_PATH,
) -> None:
    global _LOAD_ENV_FILE, _ENV_FILE_NAME, _ENV_FILE_PATH

    _LOAD_ENV_FILE = load_file

    if file_name and file_path:
        _ENV_FILE_PATH = pathlib.Path(file_path) / file_name
        _ENV_FILE_NAME = file_name

    elif file_name is not None:
        _ENV_FILE_NAME = file_name

    elif file_path is not None:
        _ENV_FILE_PATH = pathlib.Path(file_path)

    if _ENV_FILE_PATH is not None and not _ENV_FILE_PATH.exists():
        raise FileNotFoundError(f"Env file '{_ENV_FILE_PATH!s}' not found")


if typing.TYPE_CHECKING:
    from telegrinder.msgspec_utils import json
else:
    json = _json()


__all__ = (
    "LOG_SCOPE",
    "FileHandlerConfig",
    "LoggingStyleAdapter",
    "configure_dotenv",
    "json",
    "log_scope",
    "logger",
    "setup_logger",
    "take_env",
)
