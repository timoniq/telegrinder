import pathlib
import typing

import msgspec


def dec_hook(x: type[typing.Any], obj: typing.Any) -> typing.Any:
    if issubclass(x, pathlib.Path) and isinstance(obj, str | pathlib.Path):
        return x(obj)
    raise TypeError


class ObjectsIdByDefaultField(msgspec.Struct):
    name: str
    nbytes: int


class ObjectsIdByDefault(msgspec.Struct):
    object_name: str
    fields: list[ObjectsIdByDefaultField]


class ObjectsFieldsLiteralTypesField(msgspec.Struct):
    name: str
    literals: list[str | int] = msgspec.field(default_factory=lambda: [])
    enum: str | None = None
    default: str | None = None

    @property
    def enum_default(self) -> str | None:
        if self.enum is not None and self.default is not None:
            return f"{self.enum}.{self.default}"
        return None

    @property
    def literals_default(self) -> str | None:
        if self.enum is None and self.default is not None:
            return self.default
        return None


class ObjectsFieldsLiteralTypes(msgspec.Struct):
    object_name: str
    fields: list[ObjectsFieldsLiteralTypesField]


class GeneratorObjects(msgspec.Struct):
    id_by_default: list[ObjectsIdByDefault] = msgspec.field(name="id-by-default")
    fields_literal_types: list[ObjectsFieldsLiteralTypes] = msgspec.field(name="fields-literal-types")


class MethodsParamsLiteralTypesParam(ObjectsFieldsLiteralTypesField):
    pass


class MethodsParamsLiteralTypes(msgspec.Struct):
    method_name: str
    params: list[MethodsParamsLiteralTypesParam]


class GeneratorMethods(msgspec.Struct):
    params_literal_types: list[MethodsParamsLiteralTypes] = msgspec.field(name="params-literal-types")


class TypedDefaultParameter(msgspec.Struct):
    name: str
    type: str


class GeneratorAPI(msgspec.Struct):
    typed_default_parameters: list[TypedDefaultParameter] = msgspec.field(name="typed-default-parameters")


class Generator(msgspec.Struct):
    api: GeneratorAPI
    objects: GeneratorObjects
    methods: GeneratorMethods
    directory: pathlib.Path
    nicifications_path: pathlib.Path | None = None


class TelegramBotAPI(msgspec.Struct):
    version: str
    schema_url: str

    @property
    def version_number(self) -> float:
        return float(self.version.removeprefix("v"))


class Config(msgspec.Struct):
    telegram_bot_api: TelegramBotAPI = msgspec.field(name="telegram-bot-api")
    generator: Generator


__all__ = ("Config",)
