import pathlib
import typing

import msgspec

from .types.methods import GeneratorMethods
from .types.objects import GeneratorObjects


def dec_hook(x: type[typing.Any], obj: typing.Any) -> typing.Any:
    if issubclass(x, pathlib.Path) and isinstance(obj, str | pathlib.Path):
        return x(obj)
    raise TypeError


class TelegramBotAPI(msgspec.Struct):
    version: str
    schema_url: str

    @property
    def version_number(self) -> float:
        return float(self.version.removeprefix("v"))


class TypedDefaultParameter(msgspec.Struct):
    name: str
    type: str


class GeneratorAPI(msgspec.Struct):
    typed_default_parameters: list[TypedDefaultParameter] = msgspec.field(
        name="typed-default-parameters",
        default_factory=list,
    )


class Generator(msgspec.Struct):
    directory: pathlib.Path
    api: GeneratorAPI = msgspec.field(default_factory=lambda: GeneratorAPI())
    objects: GeneratorObjects = msgspec.field(default_factory=lambda: GeneratorObjects())
    methods: GeneratorMethods = msgspec.field(default_factory=lambda: GeneratorMethods())
    nicifications_path: pathlib.Path | None = None


class Config(msgspec.Struct):
    telegram_bot_api: TelegramBotAPI = msgspec.field(name="telegram-bot-api")
    generator: Generator


__all__ = (
    "Config",
    "Generator",
    "GeneratorAPI",
    "TelegramBotAPI",
    "TypedDefaultParameter",
)
