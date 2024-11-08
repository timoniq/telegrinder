import dataclasses
import datetime
import keyword
import os
import pathlib
import re
import typing
from abc import ABC, abstractmethod

import msgspec
import requests

from .merge_shortcuts import merge
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
    "to upload a new one using multipart/form-data under <file_attach_name> name."
)
MAIN_DIR: typing.Final[str] = "typegen"


def get_bot_api_schema() -> "TelegramBotAPISchema":
    logger.debug(f"Getting schema from {URL!r}")
    dct: dict[str, typing.Any] = msgspec.json.decode(requests.get(URL).text)
    dct["methods"] = [d for d in dct["methods"].values()]
    dct["types"] = [d for d in dct["types"].values()]
    logger.debug(
        "Schema (version={!r}, release_date={!r}) successfully decoded!".format(
            dct["version"],
            dct["release_date"],
        )
    )
    return msgspec.convert(dct, TelegramBotAPISchema)


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
            s = s.strip() + sep
            line = 0
    return s.rstrip()


def makesafe(s: str) -> str:
    return s + "_" if keyword.iskeyword(s) else s


def sort_all(path: pathlib.Path) -> None:
    files = tuple(str(p) for p in path.iterdir() if p.is_file() and p.suffix == ".py")
    os.system(f"sort-all {' '.join(files)}")


def to_optional(st: str) -> str:
    if '"' in st:
        return '"{} | None"'.format(st.replace('"', ""))
    return st + " | None"


def convert_to_python_type(
    tp: str,
    parent_types: dict[str, list[str]] | None = None,
    as_forward_ref: bool = False,
    as_union: bool = False,
) -> str:
    if tp.startswith("Array of"):
        return "list[{}]".format(
            " | ".join(
                convert_to_python_type(t, parent_types, as_forward_ref, as_union)
                for t in tp.removeprefix("Array of ").split(", ")
            )
        )

    if tp.startswith("typing.Literal"):
        return tp

    parent_types = parent_types or {}
    hint = '"{}"' if as_forward_ref else "{}"

    if tp in TYPES:
        return TYPES[tp]
    return (
        hint.format(tp)
        if tp not in parent_types
        else (
            "Variative[%s]" % ", ".join(hint.format(x) for x in parent_types[tp])
            if not as_union
            else hint.format(" | ".join(x for x in parent_types[tp]))
        )
    )


def camel_to_snake(s: str) -> str:
    return "".join("_" + x.lower() if x.isupper() else x for x in s)


def camel_to_pascal(s: str) -> str:
    return (s[0].upper() if s[0].islower() else s[0]) + s[1:]


def read_config_literals(path: str | None = None) -> "ConfigLiteralTypes":
    path = path or MAIN_DIR + "/config_literal_types.json"
    return msgspec.json.decode(pathlib.Path(path).read_text(encoding="UTF-8"), type=ConfigLiteralTypes)


def read_config_default_api_params(path: str | None = None) -> "ConfigDefaultAPIParams":
    path = path or MAIN_DIR + "/config_default_api_params.json"
    return msgspec.json.decode(pathlib.Path(path).read_text(encoding="UTF-8"), type=ConfigDefaultAPIParams)


def read_config_generation_id_by_default(path: str | None = None) -> "ConfigGenerationIdByDefault":
    path = path or MAIN_DIR + "/config_generation_id_by_default.json"
    return msgspec.json.decode(
        pathlib.Path(path).read_text(encoding="UTF-8"),
        type=ConfigGenerationIdByDefault,
    )


def is_unixtime_type(name: str, types: list[str], description: str) -> bool:
    return (
        "date" in name
        and "Integer" in types
        and any(x in description.lower() for x in ("unix timestamp", "unix time"))
    )


@dataclasses.dataclass(kw_only=True)
class ConfigLiteralTypes:
    objects: list["ConfigObjectLiteralTypes"] = dataclasses.field(default_factory=lambda: [])
    methods: list["ConfigMethodLiteralTypes"] = dataclasses.field(default_factory=lambda: [])


@dataclasses.dataclass(kw_only=True)
class FieldLiteralTypes:
    name: str
    """Field name."""

    enum: str | None = None
    """Optional. Reference to enumeration."""

    literals: list[str | int] = dataclasses.field(default_factory=lambda: [])
    """Optional. List with enumeration literals."""


@dataclasses.dataclass(kw_only=True)
class ParamLiteralTypes:
    name: str
    """Param name."""

    enum: str | None = None
    """Optional. Reference to enumeration."""

    literals: list[str | int] = dataclasses.field(default_factory=lambda: [])
    """Optional. List with enumeration literals."""


@dataclasses.dataclass(kw_only=True)
class ConfigObjectLiteralTypes:
    """Configuration object fields literal types."""

    name: str
    """Object name."""

    fields: list[FieldLiteralTypes] = dataclasses.field(default_factory=lambda: [])
    """Object fields."""


@dataclasses.dataclass(kw_only=True)
class ConfigMethodLiteralTypes:
    """Configuration method params literal types."""

    name: str
    """Method name."""

    params: list[ParamLiteralTypes] = dataclasses.field(default_factory=lambda: [])
    """Method params."""


@dataclasses.dataclass(kw_only=True)
class ConfigObjectsGenerationIdByDefault:
    name: str
    fields: dict[str, int]


@dataclasses.dataclass(kw_only=True)
class ConfigGenerationIdByDefault:
    objects: list[ConfigObjectsGenerationIdByDefault] = dataclasses.field(default_factory=lambda: [])


class DefaultAPIParam(typing.TypedDict):
    name: str
    type: str


class ConfigDefaultAPIParams(typing.TypedDict):
    default_params: list[DefaultAPIParam]


class ABCGenerator(ABC):
    @abstractmethod
    def generate(self, path: str) -> None:
        pass


class ObjectGenerator(ABCGenerator):
    def __init__(
        self,
        objects: list[ObjectSchema],
        nicification_path: str | None = None,
        config_generation_id_by_default: ConfigGenerationIdByDefault | None = None,
        config_literal_types: list[ConfigObjectLiteralTypes] | None = None,
    ) -> None:
        self.objects = objects
        self.nicification_path = nicification_path
        self.config_literal_types = config_literal_types or []
        self.config_generation_id_by_default = config_generation_id_by_default
        self.parent_types: dict[str, list[str]] = {obj.name: obj.subtypes for obj in objects if obj.subtypes}

    def get_field_literal_types(self, object_name: str, field_name: str) -> FieldLiteralTypes | None:
        for cfg in self.config_literal_types:
            if cfg.name == object_name:
                for ref_field in cfg.fields:
                    if ref_field.name == field_name:
                        return ref_field
        return None

    def get_field_generation_id_by_default(self, object_name: str, field_name: str) -> tuple[str, int] | None:
        if self.config_generation_id_by_default is None:
            return None

        for obj in self.config_generation_id_by_default.objects:
            if object_name == obj.name and field_name in obj.fields:
                return (field_name, obj.fields[field_name])

        return None

    def make_object_field(self, field: ObjectField, literal_types: FieldLiteralTypes | None = None) -> str:
        code = makesafe(field.name) + ": "
        field_type = "typing.Any"
        field_value = (
            "field(default=Nothing, converter={converter})"
            if not field.required
            else "field(converter={converter})"
        )

        if literal_types is not None and any((literal_types.enum, literal_types.literals)):
            literal_type_hint = literal_types.enum or "typing.Literal[%s]" % ", ".join(
                f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.literals
            )
            if len(literal_types.literals) > 3:
                literal_type_hint = literal_type_hint.replace("]", ",]")

            field_type = (
                f"list[{literal_type_hint}]"
                if any("Array of" in x for x in field.types)
                else literal_type_hint
            )
            field_value = (
                "field(default={})".format(field.default)
                if field.required and field.default is not None
                else "field()"
                if field.required
                else "field(default=Nothing)"
            )
        else:
            if field.description:
                if is_unixtime_type(field.name, field.types, field.description):
                    field.types.remove("Integer")
                    field_type = "datetime"
                    field_value = (
                        "field(default=Nothing, converter=From[datetime | None])"
                        if not field.required
                        else "field()"
                    )

                elif "InputFile" not in field.types and INPUTFILE_DOCSTRING in field.description:
                    field.types.insert(0, "InputFile")

            if len(field.types) > 1:
                field_type = "Variative[%s]" % ", ".join(
                    convert_to_python_type(tp, self.parent_types) for tp in field.types
                )
                union_types = " | ".join(
                    convert_to_python_type(tp, self.parent_types, as_union=True, as_forward_ref=True)
                    for tp in field.types
                )
                if '"' in union_types:
                    union_types = '"{}"'.format(union_types.replace('"', ""))
                field_value = field_value.format(
                    converter="From[%s]" % (to_optional(union_types) if not field.required else union_types)
                )

            elif len(field.types) == 1:
                field_type = convert_to_python_type(field.types[0], self.parent_types)
                converted_type = convert_to_python_type(
                    field.types[0], self.parent_types, as_forward_ref=True, as_union=True
                )
                field_value = (
                    field_value.format(
                        converter="From[%s]"
                        % (to_optional(converted_type) if not field.required else converted_type),
                    )
                    if ("|" in converted_type or not field.required)
                    else "field()"
                )

        if not field.required:
            field_type = f"Option[{field_type}]"

        if field.default_factory is not None:
            field_value = field_value.replace(")", f"default_factory={field.default_factory},)")

        code += f"{field_type} = {field_value}"
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
            for f in object_schema.fields:
                literal_types = self.get_field_literal_types(object_name, f.name)
                if literal_types is not None and literal_types.literals and f.required:
                    f.default = (
                        f'"{literal_types.literals[0]}"'
                        if isinstance(literal_types.literals[0], str)
                        else str(literal_types.literals[0])
                    )

                generation_id_by_default = self.get_field_generation_id_by_default(object_name, f.name)
                if generation_id_by_default is not None:
                    f.default_factory = "lambda: secrets.token_urlsafe({bytes})".format(
                        bytes=generation_id_by_default[1]
                    )

            code += TAB
            for field in (
                *filter(
                    lambda f: f.default is None and f.default_factory is None and f.required,
                    object_schema.fields,
                ),
                *filter(lambda f: f.default is not None, object_schema.fields),
                *filter(lambda f: f.default_factory is not None, object_schema.fields),
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
            "from __future__ import annotations\n\n",
            "import pathlib\n",
            "import secrets\n",
            "import typing\n\n",
            "from fntypes.variative import Variative\n",
            "from telegrinder.model import From, Model, field, generate_random_id\n",
            "from functools import cached_property\n",
            "from telegrinder.msgspec_utils import Nothing, Option, datetime\n\n",
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
        config_default_api_params: list[DefaultAPIParam] | None = None,
        *,
        api_version: str | None = None,
        release_date: str | None = None,
    ) -> None:
        self.methods = methods
        self.parent_types = parent_types
        self.config_literal_types = config_literal_types or []
        self.config_default_api_params = config_default_api_params or []
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
            return convert_to_python_type(types[0], parent_types)
        if len([x for x in types if x.startswith("Array of")]) > 1:
            array_of_types = [
                types.remove(v) or v.removeprefix("Array of") for v in types[:] if v.startswith("Array of")
            ]
            types.append("Array of " + ", ".join(array_of_types))
        sep = ", " if is_return_type else " | "
        return ("Variative[%s]" if is_return_type else "%s") % sep.join(
            convert_to_python_type(tp, parent_types) for tp in types
        )

    def get_param_literal_types(
        self,
        method_name: str,
        param_name: str,
    ) -> ParamLiteralTypes | None:
        for cfg in self.config_literal_types:
            if cfg.name == method_name:
                for param in cfg.params:
                    if param.name == param_name:
                        return param
        return None

    def get_default_param(self, name: str) -> DefaultAPIParam | None:
        name = makesafe(name)
        for param in self.config_default_api_params:
            if param["name"] == name:
                return param
        return None

    def make_method_body(self, method_schema: MethodSchema) -> str:
        field_descriptions = filter(
            None,
            [
                (
                    f":param {makesafe(x.name)}: "
                    + chunks_str(
                        x.description + ("." if not x.description.endswith(".") else ""),
                        sep=" \\\n" + TAB + TAB,
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
            *filter(lambda x: x.required and not self.get_default_param(x.name), params),
            *filter(lambda x: not x.required or self.get_default_param(x.name), params),
        ):
            literal_types = self.get_param_literal_types(method_name, p.name)
            param_name = makesafe(p.name)

            if literal_types is not None:
                tp = literal_types.enum or "typing.Literal[%s]" % ", ".join(
                    f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.literals
                )
                p.types = [tp]

            if p.description and is_unixtime_type(param_name, p.types, p.description):
                p.types.insert(p.types.index("Integer"), "Unixtime")

            default_param_value = (
                None if self.get_default_param(param_name) is None else f'default_params["{param_name}"]'
            )
            code = f"{TAB * 2}{param_name}: "

            if not p.required or default_param_value:
                code += f"{self.make_type_hint(p.types)} {'| None ' if not p.required else ''}= {default_param_value}"
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
            + ("*,\n" if method_schema.params else "")
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
                '    """Telegram {}, released `{}`."""\n\n'.format(
                    (self.api_version or "Bot API x.x").replace("Bot API", "Bot API methods version"),
                    self.release_date or datetime.datetime.now().ctime(),
                )
            )
        )
        default_params_typeddict = 'typing.TypedDict("DefaultParams", {})'.format(
            "{%s}"
            % ", ".join(
                f""""{x['name']}": {convert_to_python_type(x['type'], parent_types=self.parent_types)}"""
                for x in self.config_default_api_params
            )
        )
        lines = [
            "import typing\n",
            "from datetime import datetime\n\n"
            "from fntypes.co import Result, Variative\n"
            "from telegrinder.api.error import APIError\n",
            "from telegrinder.model import ProxiedDict, full_result, get_params\n",
            "from telegrinder.types.enums import *  # noqa: F403\n"
            "from telegrinder.types.objects import *  # noqa: F403\n\n"
            "if typing.TYPE_CHECKING:\n",
            "    from telegrinder.api.api import API\n\n\n",
            "class APIMethods:\n" + docstring,
            f"\n\n    default_params = ProxiedDict({default_params_typeddict})\n\n",
            '    def __init__(self, api: "API") -> None:\n',
            "        self.api = api\n\n",
        ]

        for method_schema in self.methods:
            lines.append(self.make_method(method_schema) + "\n\n")

        with open(path + "/methods.py", mode="w", encoding="UTF-8") as f:
            lines.append('\n\n\n__all__ = ("APIMethods",)\n\n')
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
    path_config_default_api_params: str | None = None,
    path_config_generation_id_by_default: str | None = None,
    path_nicifications: str | None = None,
    object_generator: ABCGenerator | None = None,
    method_generator: ABCGenerator | None = None,
) -> None:
    path_dir = path_dir or "telegrinder/types"
    if not os.path.exists(path_dir):
        logger.warning(f"Path dir {path_dir!r} not found. Making dir...")
        os.makedirs(path_dir)

    if object_generator is None or method_generator is None:
        schema = get_bot_api_schema()
        cfg_literal_types = read_config_literals(path_config_literals)
        object_generator = object_generator or ObjectGenerator(
            objects=schema.objects,
            nicification_path=MAIN_DIR + (path_nicifications or "/nicifications.py"),
            config_literal_types=cfg_literal_types.objects,
            config_generation_id_by_default=read_config_generation_id_by_default(
                path_config_generation_id_by_default
            ),
        )
        method_generator = method_generator or MethodGenerator(
            methods=schema.methods,
            parent_types=(
                object_generator.parent_types if isinstance(object_generator, ObjectGenerator) else {}
            ),
            config_literal_types=cfg_literal_types.methods,
            config_default_api_params=read_config_default_api_params(path_config_default_api_params)[
                "default_params"
            ],
            api_version=schema.version,
            release_date=schema.release_date,
        )

    object_generator.generate(path_dir)
    method_generator.generate(path_dir)
    logger.info("Schema has been successfully generated.")

    logger.debug("Run sort-all...")
    sort_all(pathlib.Path(path_dir))
    logger.info("Sort-all successfully sorted __all__ in files.")

    logger.debug("Run ruff formatter...")
    if os.system(f"ruff format {path_dir}") != 0:
        logger.error("Ruff formatter failed.")
    else:
        logger.info("Ruff formatter successfully formatted files.")

    logger.debug("Run ruff-isort...")
    if os.system(f"ruff check {path_dir} --select I --select F401 --fix") != 0:
        logger.error("ruff-isort failed.")
    else:
        logger.info("Ruff-isort successfully sorted imports.")

    merge()


__all__ = (
    "ABCGenerator",
    "ConfigLiteralTypes",
    "ConfigMethodLiteralTypes",
    "ConfigObjectLiteralTypes",
    "FieldLiteralTypes",
    "MethodGenerator",
    "ObjectGenerator",
    "ParamLiteralTypes",
    "find_nicifications",
    "generate",
    "get_bot_api_schema",
    "read_config_literals",
    "sort_all",
)
