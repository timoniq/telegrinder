import datetime
import os
import pathlib
import re
import typing
from abc import ABC, abstractmethod

import msgspec
import requests

from .models import (
    MethodParameter,
    MethodSchema,
    ObjectField,
    ObjectSchema,
    TelegramBotAPISchema,
)

try:
    from telegrinder.modules import logger
except ImportError:
    import logging

    logger = logging.getLogger("typegen")

ModelT = typing.TypeVar("ModelT", bound=msgspec.structs.Struct)

JSON_DECODER: typing.Final[msgspec.json.Decoder[typing.Any]] = msgspec.json.Decoder(strict=True)
URL: typing.Final[str] = "https://raw.githubusercontent.com/PaulSonOfLars/telegram-bot-api-spec/main/api.json"
TAB: typing.Final[str] = "    "
TYPES: typing.Final[dict[str, str]] = {
    "String": "str",
    "Integer": "int",
    "Float": "float",
    "Boolean": "bool",
    "Unixtime": "datetime",
}
INPUTFILE_DOCSTRING: typing.Final[str] = (
    "to upload a new one using multipart/form-data" " under <file_attach_name> name."
)
MAIN_DIR: typing.Final[str] = "typegen"


def get_schema_json() -> "SchemaJson":
    logger.debug(f"Sending a get request {URL!r}")
    raw = requests.get(URL).text
    dct: dict[str, typing.Any] = JSON_DECODER.decode(raw)
    dct["methods"] = [d for d in dct["methods"].values()]
    dct["types"] = [d for d in dct["types"].values()]
    logger.debug(
        "Schema (version={!r}, release_date={!r}) successfully decoded!".format(
            dct["version"],
            dct["release_date"],
        )
    )
    return typing.cast(SchemaJson, dct)


def find_nicifications(name: str, path: str) -> tuple[str | None, list[str]]:
    with open(path, mode="r", encoding="UTF-8") as f:
        ns = f.read()
    regex = r"class _" + name + r"\((?P<base>.+)\):\n((?:.|\n {4}|\n$)+)"
    matches = list(re.finditer(regex, ns, flags=re.MULTILINE))
    if matches:
        return matches[0].group("base"), [match.group(2) for match in matches]
    return None, []


def chunks_str(s: str, sep: str = "\n"):
    words = s.split()
    s = ""
    line = 0
    for word in words:
        s += word + " "
        line += len(word)
        if line >= 60:
            s += sep
            line = 0
    return s.rstrip()


def sort_all(path: pathlib.Path) -> None:
    files = tuple(str(p) for p in path.iterdir() if p.is_file() and p.suffix == ".py")
    os.system(f"sort-all {' '.join(files)}")


def convert_to_python_type(
    tp: str,
    parent_types: dict[str, list[str]] | None = None,
    as_forward_ref: bool = True,
) -> str:
    if tp.startswith("Array of"):
        return "list[{}]".format(
            " | ".join(
                convert_to_python_type(t, parent_types, as_forward_ref=as_forward_ref)
                for t in tp.removeprefix("Array of ").split(", ")
            )
        )
    if tp.startswith("typing.Literal"):
        return tp
    parent_types = parent_types or {}
    hint = '"{}"' if as_forward_ref else "{}"
    return TYPES.get(
        tp,
        (
            hint.format(tp)
            if tp not in parent_types
            else "Variative[%s]" % ", ".join(hint.format(x) for x in parent_types[tp])
        ),
    )


def camel_to_snake(s: str) -> str:
    return "".join("_" + x.lower() if x.isupper() else x for x in s)


def camel_to_pascal(s: str) -> str:
    return (s[0].upper() if s[0].islower() else s[0]) + s[1:]


def convert_schema_to_model(schema_json: "SchemaJson", model: type[ModelT]) -> ModelT:
    logger.debug(f"Converting to model {model.__name__!r}...")
    schema = msgspec.convert(schema_json, type=model)
    logger.debug(f"Schema successfully converted to model {model.__name__!r}!")
    return schema


def read_config_literals(path: str | None = None) -> "ConfigLiteralTypes":
    path = path or MAIN_DIR + "/config_literal_types.json"
    with open(path, mode="r", encoding="UTF-8") as f:
        return JSON_DECODER.decode(f.read())


def is_unixtime_type(name: str, types: list[str], description: str) -> bool:
    return (
        "date" in name
        and "Integer" in types
        and any(x in description.lower() for x in ("unix timestamp", "unix time"))
    )


class SchemaJson(typing.TypedDict):
    version: str
    release_date: str
    changelog: str
    methods: list[dict[str, typing.Any]]
    types: list[dict[str, typing.Any]]


class ConfigLiteralTypes(typing.TypedDict, total=True):
    objects: typing.NotRequired[list["ConfigObjectLiteralTypes"]]
    methods: typing.NotRequired[list["ConfigMethodLiteralTypes"]]


class FieldLiteralTypes(typing.TypedDict, total=True):
    """Mapping containing field name, reference to enumeration and specific enumeration literals."""

    name: str
    """Field name."""

    enum: typing.NotRequired[str]
    """Optional. Reference to enumeration."""

    literals: typing.NotRequired[list[str | int]]
    """Optional. List with enumeration literals."""


class ParamLiteralTypes(typing.TypedDict, total=True):
    """Mapping containing param name, reference to enumeration and specific enumeration literals."""

    name: str
    """Param name."""

    enum: typing.NotRequired[str]
    """Optional. Reference to enumeration."""

    literals: typing.NotRequired[list[str | int]]
    """Optional. List with enumeration literals."""


class ConfigObjectLiteralTypes(typing.TypedDict):
    """Configuration object fields literal types."""

    name: str
    """Object name."""

    fields: list[FieldLiteralTypes]
    """Object fields."""


class ConfigMethodLiteralTypes(typing.TypedDict):
    """Configuration method params literal types."""

    name: str
    """Method name."""

    params: list[ParamLiteralTypes]
    """Method params."""


class ABCGenerator(ABC):
    @abstractmethod
    def generate(self, path: str) -> None:
        pass


class ObjectGenerator(ABCGenerator):
    def __init__(
        self,
        objects: list[ObjectSchema],
        nicification_path: str | None = None,
        config_literal_types: list[ConfigObjectLiteralTypes] | None = None,
    ) -> None:
        self.objects = objects
        self.rename_field_names = {
            "from": "from_",
            "for": "for_",
            "in": "in_",
        }
        self.nicification_path = nicification_path
        self.config_literal_types = config_literal_types or []
        self.parent_types: dict[str, list[str]] = {obj.name: obj.subtypes for obj in objects if obj.subtypes}

    def get_field_literal_types(self, object_name: str, field_name: str) -> FieldLiteralTypes | None:
        for cfg in self.config_literal_types:
            if cfg["name"] == object_name:
                for ref_field in cfg["fields"]:
                    if ref_field["name"] == field_name:
                        return ref_field
        return None

    def make_object_field(self, field: ObjectField, literal_types: FieldLiteralTypes | None = None) -> str:
        code = f"{self.rename_field_names.get(field.name, field.name)}: "
        field_type = "typing.Any"

        if literal_types is not None and any(x in literal_types for x in ("literals", "enum")):
            literal_type_hint = literal_types.get("enum") or "typing.Literal[%s]" % ", ".join(
                f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.get("literals", [])
            )
            if len(literal_types.get("literals", [])) > 3:
                literal_type_hint = literal_type_hint.replace("]", ",]")
            field_type = (
                f"list[{literal_type_hint}]"
                if any("Array of" in x for x in field.types)
                else literal_type_hint
            )
        else:
            if field.description:
                if is_unixtime_type(field.name, field.types, field.description):
                    field.types.remove("Integer")
                    field_type = "datetime"

                elif "InputFile" not in field.types and INPUTFILE_DOCSTRING in field.description:
                    field.types.insert(0, "InputFile")

            if len(field.types) > 1:
                field_type = "Variative[%s]" % ", ".join(
                    convert_to_python_type(tp, self.parent_types) for tp in field.types
                )

            elif len(field.types) == 1:
                field_type = convert_to_python_type(field.types[0], self.parent_types)

        if not field.required and field_type:
            field_type = f"Option[{field_type}] = Nothing"

        code += field_type
        if field.description:
            description = field.description.replace('"', "`")
            sep = "\n" + TAB
            code += (
                f'{sep}"""{chunks_str(description, sep=sep)}'
                f'{"." if not description.endswith(".") else ""}"""\n'
            )

        return code

    def make_subtype_of(self, subtype_of: list[str]) -> str:
        return "Model" if not subtype_of else ", ".join(subtype_of)

    def make_object(self, object_schema: ObjectSchema) -> str:
        object_name = camel_to_pascal(object_schema.name)

        if self.nicification_path:
            base, nicifications = find_nicifications(object_name, self.nicification_path)
        else:
            base, nicifications = None, []

        sybtypes_of = self.make_subtype_of(object_schema.subtype_of or [])
        code = (
            f"class {camel_to_pascal(object_schema.name)}"
            f"({base if base and base != object_name else sybtypes_of}):\n{TAB}"
        )
        description = (
            "Base object"
            if object_schema.subtypes
            else ("Object" if base is None or base == object_name else base.split(".")[-1] + " object")
        ) + f" `{object_name}`, see the [documentation]({object_schema.href})."
        code += '"""%s\n\n%s\n"""' % (
            description,
            (
                "No description yet."
                if not object_schema.description
                else "\n".join(object_schema.description)
            ),
        )

        code += f"\n"
        if not object_schema.fields and not nicifications:
            if (not object_schema.subtypes and base is None) or not object_schema.subtypes:
                logger.warning(f"Object {object_name!r} has not fields, subtypes and nicification.")
            code += f"{TAB}pass" if not object_schema.description else ""
            return code

        if object_schema.fields:
            code += TAB
            for field in (
                *filter(lambda f: f.required, object_schema.fields),
                *filter(lambda f: not f.required, object_schema.fields),
            ):
                literal_types = self.get_field_literal_types(object_name, field.name)
                code += f"\n{TAB}" + self.make_object_field(field, literal_types)

        if nicifications:
            for n in nicifications:
                if object_schema.fields:
                    for f, t, d in re.findall(r'(\b\w+\b):\s*(.+)\s*"""(.*?)"""', n, flags=re.DOTALL):
                        new_code = f'\n    {f}: {t.strip()}\n    """{d}"""'
                        code = re.sub(r"\n    " + f + r": .+((?:.|\n {4}|\n$)+)", new_code, code)
                        n = n.replace(new_code.strip(), "")
                code += n

        return code

    def generate(self, path: str) -> None:
        if not self.objects:
            logger.error("Objects is empty.")
            exit(-1)

        logger.debug("Generate objects...")
        lines = [
            "import typing\n\n",
            "from fntypes.co import Some, Variative\n",
            "from telegrinder.model import Model\n",
            "from telegrinder.msgspec_utils import Option, Nothing, datetime\n\n",
        ]
        all_ = ["Model"]

        if self.config_literal_types:
            lines.append("from telegrinder.types.enums import *  # noqa: F403\n")

        for object_schema in sorted(self.objects, key=lambda x: x.subtypes or [], reverse=True):
            lines.append(self.make_object(object_schema) + "\n\n")
            all_.append(camel_to_pascal(object_schema.name))

        lines.append(f"\n__all__ = {tuple(all_)!r}\n")
        with open(path + "/objects.py", mode="w", encoding="UTF-8") as f:
            f.writelines(lines)

        exec(f"from {path.replace('/', '.') + '.enums'} import __all__", globals(), locals())
        with open(path + "/__init__.py", "w", encoding="UTF-8") as f:
            f.writelines(
                [
                    "from telegrinder.types.enums import *\n",
                    "from telegrinder.types.objects import *\n\n",
                    f"__all__ = {locals()['__all__'] + tuple(all_)}\n",  # type: ignore
                ]
            )

        logger.info(
            "Generation of {} objects into {!r} has been completed.",
            len(self.objects),
            path + "/objects.py",
        )


class MethodGenerator(ABCGenerator):
    def __init__(
        self,
        methods: list[MethodSchema],
        parent_types: dict[str, list[str]],
        config_literal_types: list[ConfigMethodLiteralTypes] | None = None,
        *,
        api_version: str | None = None,
        release_date: str | None = None,
    ) -> None:
        self.methods = methods
        self.parent_types = parent_types
        self.config_literal_types = config_literal_types or []
        self.api_version = api_version
        self.release_date = release_date

    @staticmethod
    def make_type_hint(
        types: list[str],
        parent_types: dict[str, list[str]] | None = None,
        is_return_type: bool = False,
    ) -> str:
        if not types:
            return "typing.Any"
        if len(types) == 1:
            return convert_to_python_type(types[0], parent_types, as_forward_ref=False)
        if len([x for x in types if x.startswith("Array of")]) > 1:
            array_of_types = [
                types.remove(v) or v.removeprefix("Array of") for v in types[:] if v.startswith("Array of")
            ]
            types.append("Array of " + ", ".join(array_of_types))
        sep = ", " if is_return_type else " | "
        return ("Variative[%s]" if is_return_type else "%s") % sep.join(
            convert_to_python_type(tp, parent_types, as_forward_ref=False) for tp in types
        )

    def get_param_literal_types(
        self,
        method_name: str,
        param_name: str,
    ) -> ParamLiteralTypes | None:
        for cfg in self.config_literal_types:
            if cfg["name"] == method_name:
                for param in cfg["params"]:
                    if param["name"] == param_name:
                        return param
        return None

    def make_method_body(self, method_schema: MethodSchema) -> str:
        field_descriptions = filter(
            None,
            [
                (
                    f":param {x.name}: "
                    + chunks_str(
                        x.description + ("." if not x.description.endswith(".") else ""),
                        sep="\\\n" + TAB + TAB,
                    ).replace('"', "`")
                    if x.description
                    else ""
                )
                for x in method_schema.params or []
            ],
        )
        return (
            '"""'
            + (
                f"Method `{method_schema.name}`, see the [documentation]({method_schema.href})\n\n{TAB * 2}"
                + chunks_str(f"{TAB}\n".join(method_schema.description or []), sep="\n" + TAB + TAB)
                + f"\n\n{TAB * 2}"
                + (f"\n\n{TAB * 2}".join(field_descriptions)).strip()
            ).strip()
            + f'\n{TAB * 2}"""\n\n'
            + '{}method_response = await self.api.request_raw("{}", get_params(locals()),)\n'.format(
                TAB * 2,
                method_schema.name,
            )
            + f"{TAB * 2}return full_result(method_response, "
            + f"{self.make_type_hint(method_schema.returns or [], self.parent_types, is_return_type=True)})"
        )

    def make_method_params(self, method_name: str, params: list[MethodParameter] | None = None) -> list[str]:
        result = []
        if not params:
            return result

        for p in (
            *filter(lambda x: x.required, params),
            *filter(lambda x: not x.required, params),
        ):
            literal_types = self.get_param_literal_types(method_name, p.name)

            if literal_types is not None:
                tp = (
                    literal_types["enum"]
                    if "enum" in literal_types
                    else "typing.Literal[%s]"
                    % ", ".join(
                        f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.get("literals", [])
                    )
                )
                p.types = [tp]

            if p.description and is_unixtime_type(p.name, p.types, p.description):
                p.types.insert(p.types.index("Integer"), "Unixtime")

            code = f"{TAB * 2}{p.name}: "
            if not p.required:
                type_hint = self.make_type_hint(p.types)
                code += f"{type_hint} | None = None"
            else:
                code += self.make_type_hint(p.types)
            result.append(code)

        return result

    def make_return_type(self, returns: list[str] | None = None) -> str:
        if not returns:
            return "Result[bool, APIError]"
        return f"Result[{self.make_type_hint(returns, self.parent_types, is_return_type=True)}, APIError]"

    def make_method(self, method_schema: MethodSchema) -> str:
        code = (
            f"{TAB}async def {camel_to_snake(method_schema.name)}(self,"
            + ",\n".join(self.make_method_params(method_schema.name, method_schema.params))
            + ("," if method_schema.params else "")
            + f"**other: typing.Any{',' if method_schema.params else ''}) -> "
            + self.make_return_type(method_schema.returns)
            + f":\n{TAB * 2}"
            + self.make_method_body(method_schema)
        )
        return code

    def generate(self, path: str) -> None:
        if not self.methods:
            logger.error("Methods is empty.")
            exit(-1)

        logger.debug("Generate methods...")
        docstring = (
            ""
            if not self.api_version or not self.release_date
            else (
                '    """Telegram {} methods, released `{}`."""\n\n'.format(
                    self.api_version or "Bot API",
                    self.release_date or datetime.datetime.now().ctime(),
                )
            )
        )
        lines = [
            "import typing\n",
            "from datetime import datetime\n\n"
            "from fntypes.co import Result, Variative\n"
            "from telegrinder.api.error import APIError\n",
            "from telegrinder.model import full_result, get_params\n",
            "from telegrinder.types.enums import *  # noqa: F403\n"
            "from telegrinder.types.objects import *  # noqa: F403\n\n"
            "if typing.TYPE_CHECKING:\n",
            "    from telegrinder.api.abc import ABCAPI\n\n\n",
            "class APIMethods:\n" + docstring,
            '    def __init__(self, api: "ABCAPI") -> None:\n',
            "        self.api = api\n\n",
        ]

        for method_schema in self.methods:
            lines.append(self.make_method(method_schema) + "\n\n")

        with open(path + "/methods.py", mode="w", encoding="UTF-8") as f:
            f.writelines(lines)

        logger.info(
            "Generation of {} methods into {!r} has been completed.",
            len(self.methods),
            path + "/objects.py",
        )


def generate(
    *,
    path_dir: str | None = None,
    path_config_literals: str | None = None,
    path_nicifications: str | None = None,
    object_generator: ABCGenerator | None = None,
    method_generator: ABCGenerator | None = None,
) -> None:
    path_dir = path_dir or "telegrinder/types"
    if not os.path.exists(path_dir):
        logger.warning(f"Path dir {path_dir!r} not found. Making dir...")
        os.makedirs(path_dir)

    if object_generator is None or method_generator is None:
        schema_json = get_schema_json()
        schema_model = convert_schema_to_model(schema_json, TelegramBotAPISchema)
        cfg_literal_types = read_config_literals(path_config_literals)
        object_generator = object_generator or ObjectGenerator(
            objects=schema_model.objects,
            nicification_path=MAIN_DIR + (path_nicifications or "/nicifications.py"),
            config_literal_types=cfg_literal_types.get("objects"),
        )
        method_generator = method_generator or MethodGenerator(
            methods=schema_model.methods,
            parent_types=(
                object_generator.parent_types if isinstance(object_generator, ObjectGenerator) else {}
            ),
            config_literal_types=cfg_literal_types.get("methods"),
            api_version=schema_json["version"],
            release_date=schema_json["release_date"],
        )

    object_generator.generate(path_dir)
    method_generator.generate(path_dir)
    logger.info("Schema has been successfully generated.")

    logger.debug("Run ruff formatter...")
    if os.system(f"ruff format {path_dir} --config pyproject.toml") != 0:
        logger.error("Ruff formatter failed.")
    else:
        logger.info("Ruff formatter successfully formatted files.")

    logger.debug("Run ruff-isort...")
    if os.system(f"ruff check {path_dir} --select I --select F401 --fix") != 0:
        logger.error("ruff-isort failed.")
    else:
        logger.info("Ruff-isort successfully sorted imports.")

    logger.debug("Run sort-all...")
    sort_all(pathlib.Path(path_dir))
    logger.info("Sort-all successfully sorted __all__ in files.")


__all__ = (
    "ABCGenerator",
    "ConfigLiteralTypes",
    "ConfigMethodLiteralTypes",
    "ConfigObjectLiteralTypes",
    "FieldLiteralTypes",
    "MethodGenerator",
    "ObjectGenerator",
    "ParamLiteralTypes",
    "SchemaJson",
    "convert_schema_to_model",
    "find_nicifications",
    "generate",
    "sort_all",
    "get_schema_json",
    "read_config_literals",
)
