import os
import pathlib
import re
import shlex
import sys
import typing

import betterconf
from kungfu import Nothing, Option, Some

VARIABLE_NAME_PATTERN: typing.Final = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
ASSIGNMENT_OPERATOR: typing.Final = "="
ENV_FILE_NAME: typing.Final = os.environ.get("TELEGRINDER_CONFIG_ENV_FILE_NAME", ".env")
LOGGER_LEVELS: typing.Final = ("DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL", "EXCEPTION")

LoggerLevel = typing.NewType("LoggerLevel", str)


def find_env_file() -> Option[pathlib.Path]:
    caller_frame = sys._getframe()

    while caller_frame:
        if caller_frame.f_back is None:
            break

        caller_frame = caller_frame.f_back

    for root, _, files in os.walk(os.path.dirname(caller_frame.f_code.co_filename)):
        if ENV_FILE_NAME in files:
            return Some(pathlib.Path(root) / ENV_FILE_NAME)

    return Nothing()


def take[T](
    name: str,
    var_type: type[T] = str,
    /,
    *,
    from_dotenv: bool = True,
) -> T:
    value = DOTENV.get(name) if from_dotenv else ENV.get(name)

    if var_type is not str:
        value = CASTERS[var_type].cast(value)

    return typing.cast("T", value)


class LoggerLevelCaster(betterconf.AbstractCaster):
    def cast(self, value: str) -> LoggerLevel:
        if value not in LOGGER_LEVELS:
            raise betterconf.ImpossibleToCastError(value, self)
        return LoggerLevel(value)


class DotenvProvider(betterconf.AbstractProvider):
    __slots__ = ("env_file", "loaded")

    env_file: pathlib.Path | None
    loaded: bool

    def __init__(self) -> None:
        self.env_file = None
        self.loaded = False

    @property
    def env_file_is_found(self) -> bool:
        return self.loaded is True and self.env_file is not None

    def load(self) -> None:
        if not self.loaded:
            self.loaded = True
            self.env_file = find_env_file().unwrap_or_none()

        if self.env_file is None:
            return

        variables: dict[str, str] = {}

        for line in self.env_file.read_text().splitlines():
            match tuple(shlex.shlex(instream=line, posix=True)):
                case (var_name, operator, *tokens) if tokens and operator == ASSIGNMENT_OPERATOR and VARIABLE_NAME_PATTERN.match(var_name):
                    variables[var_name] = "".join(tokens).replace(r"\n", "\n").replace(r"\t", "\t")
                case _:
                    continue

        os.environ.update(variables)

    def get(self, name: str) -> str:
        if not self.loaded:
            self.load()
        return ENV.get(name)


DOTENV: typing.Final = DotenvProvider()
ENV: typing.Final = betterconf.EnvironmentProvider()
CASTERS: typing.Final[dict[type[typing.Any], betterconf.AbstractCaster]] = {
    LoggerLevel: (to_logger_level := LoggerLevelCaster()),  # type: ignore
    **betterconf.caster.BUILTIN_CASTERS,
}


__all__ = ("CASTERS", "DOTENV", "ENV", "LoggerLevel", "take", "to_logger_level")
