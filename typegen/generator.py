import abc
import datetime
import importlib
import keyword
import os
import pathlib
import re
import sys
import typing

import msgspec
import requests

from .config import ConfigTOML, read_config
from .merge_shortcuts import merge_shortcuts
from .models import (
    Config,
    MethodParameter,
    MethodSchema,
    MethodsParamsLiteralTypesParam,
    ObjectField,
    ObjectSchema,
    ObjectsFieldsLiteralTypesField,
    ObjectsIdByDefaultField,
    TelegramBotAPISchema,
    TypedDefaultParameter,
    dec_hook,
)

try:
    from telegrinder.modules import logger
except ImportError:
    import logging

    logger = logging.getLogger("typegen")

TYPEGEN_DIR: typing.Final[pathlib.Path] = pathlib.Path(__file__).parent
TAB: typing.Final[str] = "    "
MAX_LENGTH_LINE_CHUNK: typing.Final[int] = 60
TYPES: typing.Final[dict[str, str]] = {
    "String": "str",
    "Integer": "int",
    "Float": "float",
    "Boolean": "bool",
    "Unixtime": "datetime",
}
INPUTFILE_DOCSTRING: typing.Final[str] = "using multipart/form-data"


def download_schema(config_toml: ConfigTOML, config_model: Config, /) -> TelegramBotAPISchema:
    logger.debug(f"Downloading schema from {config_model.telegram_bot_api.schema_url!r}...")

    schema: dict[str, typing.Any] = msgspec.json.decode(
        requests.get(config_model.telegram_bot_api.schema_url).text
    )
    schema_version = float(schema["version"].split()[-1])
    schema.update(
        dict(
            methods=[d for d in schema["methods"].values()],
            types=[d for d in schema["types"].values()],
        ),
    )

    logger.debug(
        "Schema (version={}, release_date={!r}) successfully downloaded!",
        schema_version,
        schema["release_date"],
    )

    if schema_version > config_model.telegram_bot_api.version_number:
        logger.debug("New version of the schema, upgrade version of the telegram bot api in config.")
        config_toml.document["telegram-bot-api"]["version"] = f"v{schema_version}"  # type: ignore
        config_toml.save()

    return msgspec.convert(obj=schema, type=TelegramBotAPISchema)


def find_object_nicifications(
    object_name: str, nicification_path: pathlib.Path, /
) -> tuple[str | None, list[str]]:
    pattern = r"class _" + object_name + r"\((?P<base>.+)\):\n((?:.|\n {4}|\n$)+)"
    nicifications_source = nicification_path.read_text(encoding="UTF-8")
    matches = list(re.finditer(pattern, nicifications_source, flags=re.MULTILINE))
    return (None, []) if not matches else (matches[0].group("base"), [match.group(2) for match in matches])


def chunks_str(s: str, sep: str = "\n"):
    chunked_string, line_length = "", 0

    for word in s.split():
        chunked_string += word + " "
        line_length += len(word)

        if line_length >= MAX_LENGTH_LINE_CHUNK:
            chunked_string = chunked_string.strip() + sep
            line_length = 0

    return chunked_string.rstrip()


def makesafe_name(s: str, /) -> str:
    return s + "_" if keyword.iskeyword(s) else s


def run_sort_all(path: pathlib.Path, /) -> None:
    logger.debug("Run sort-all...")
    files = tuple(str(p) for p in path.iterdir() if p.is_file() and p.suffix == ".py")
    os.system(f"sort-all {' '.join(files)}")


def run_ruff_linter(path: pathlib.Path, /) -> None:
    logger.debug("Run ruff formatter...")
    if os.system(f"ruff format {path}") != 0:
        logger.error("Ruff formatter failed.")
    else:
        logger.info("Ruff formatter successfully formatted files.")

    logger.debug("Run ruff-isort...")
    if os.system(f"ruff check {path} --select I --select F401 --fix") != 0:
        logger.error("ruff-isort failed.")
    else:
        logger.info("Ruff-isort successfully sorted imports.")


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


def is_unixtime_type(name: str, types: list[str], description: str) -> bool:
    return (
        "date" in name
        and "Integer" in types
        and any(x in description.lower() for x in ("unix timestamp", "unix time"))
    )


class ABCGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, path: pathlib.Path) -> None:
        pass


class ObjectGenerator(ABCGenerator):
    def __init__(
        self,
        objects: list[ObjectSchema],
        config: Config,
    ) -> None:
        self.objects = objects
        self.config = config
        self.parent_types: dict[str, list[str]] = {obj.name: obj.subtypes for obj in objects if obj.subtypes}

    def get_literal_types_field(self, object_name: str, field_name: str) -> ObjectsFieldsLiteralTypesField | None:
        for object_literal_types in self.config.generator.objects.fields_literal_types:
            if object_literal_types.object_name == object_name:
                for field in object_literal_types.fields:
                    if field_name == field.name:
                        return field

        return None

    def get_generation_id_by_default_field(
        self, object_name: str, field_name: str
    ) -> ObjectsIdByDefaultField | None:
        for id_by_default in self.config.generator.objects.id_by_default:
            if object_name == id_by_default.object_name:
                for field in id_by_default.fields:
                    if field_name == field.name:
                        return field

        return None

    def make_object_field(
        self,
        field: ObjectField,
        literal_types: ObjectsFieldsLiteralTypesField | None = None,
    ) -> str:
        code = makesafe_name(field.name) + ": "
        field_type = "typing.Any"
        field_value = (
            "field(default=UNSET, converter={converter})" if not field.required else "field(converter={converter})"
        )

        if literal_types is not None and any((literal_types.enum, literal_types.literals)):
            literal_type_hint = literal_types.enum or "typing.Literal[%s]" % ", ".join(
                f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.literals
            )
            if len(literal_types.literals) > 3:
                literal_type_hint = literal_type_hint.replace("]", ",]")

            field_type = (
                f"list[{literal_type_hint}]" if any("Array of" in x for x in field.types) else literal_type_hint
            )
            field_value = (
                "field(default={})".format(field.default)
                if field.required and field.default is not None
                else "field()"
                if field.required
                else "field(default=UNSET)"
            )
        else:
            if field.description:
                if is_unixtime_type(field.name, field.types, field.description):
                    field.types.remove("Integer")
                    field_type = "datetime"
                    field_value = (
                        "field(default=UNSET, converter=From[datetime | None])"
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
                f'{sep}"""{chunks_str(description, sep=sep)}{"." if not description.endswith(".") else ""}"""\n'
            )

        return code

    def make_subtype_of(self, subtype_of: list[str]) -> str:
        return "Model" if not subtype_of else ", ".join(subtype_of)

    def make_object(self, object_schema: ObjectSchema) -> str:
        object_name = camel_to_pascal(object_schema.name)

        if self.config.generator.nicifications_path is not None:
            base_object_name, nicifications = find_object_nicifications(
                object_name,
                self.config.generator.nicifications_path,
            )
        else:
            base_object_name, nicifications = None, []

        sybtypes_of = self.make_subtype_of(object_schema.subtype_of or [])
        description = (
            "Base object"
            if object_schema.subtypes
            else (
                "Object"
                if base_object_name is None or base_object_name == object_name
                else base_object_name.split(".")[-1] + " object"
            )
        ) + f" `{object_name}`, see the [documentation]({object_schema.href})."

        code = (
            f"class {camel_to_pascal(object_schema.name)}"
            f"({base_object_name if base_object_name and base_object_name != object_name else sybtypes_of}):\n{TAB}"
        )
        code += '"""%s\n\n%s\n"""' % (
            description,
            ("No description yet." if not object_schema.description else "\n".join(object_schema.description)),
        )
        code += f"\n"

        if not object_schema.fields and not nicifications:
            if (not object_schema.subtypes and base_object_name is None) or not object_schema.subtypes:
                logger.warning(
                    f"Object {object_name!r} has no fields or subtypes or nicification (mark as empty object).",
                )

            code += TAB + "pass" if not object_schema.description else ""
            return code

        if object_schema.fields:
            for f in object_schema.fields:
                literal_types = self.get_literal_types_field(object_name, f.name)
                if literal_types is not None and literal_types.literals and f.required:
                    f.default = (
                        f'"{literal_types.literals[0]}"'
                        if isinstance(literal_types.literals[0], str)
                        else str(literal_types.literals[0])
                    )

                generation_id_by_default = self.get_generation_id_by_default_field(object_name, f.name)
                if generation_id_by_default is not None:
                    f.default_factory = "lambda: secrets.token_urlsafe({nbytes})".format(
                        nbytes=generation_id_by_default.nbytes,
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
                literal_types = self.get_literal_types_field(object_name, field.name)
                code += f"\n{TAB}" + self.make_object_field(field, literal_types)

        for nicification in nicifications:
            if object_schema.fields:
                for f, t, d in re.findall(r'(\b\w+\b):\s*(.+)\s*"""(.*?)"""', nicification, flags=re.DOTALL):
                    new_code = f'\n    {f}: {t.strip()}\n    """{d}"""'
                    code = re.sub(r"\n    " + f + r": .+((?:.|\n {4}|\n$)+)", new_code, code)
                    nicification = nicification.replace(new_code.strip(), "")

            code += nicification

        return code

    def generate(self, path: pathlib.Path) -> None:
        if not self.objects:
            logger.error("Objects is empty.")
            sys.exit(-1)

        logger.debug("Generate objects...")
        lines = [
            "from __future__ import annotations\n\n",
            "import pathlib\n",
            "import secrets\n",
            "import typing\n\n",
            "from fntypes.co import Variative, Nothing\n",
            "from telegrinder.model import UNSET, From, Model, field\n",
            "from telegrinder.types.input_file import InputFile\n",
            "from functools import cached_property\n",
            "from telegrinder.msgspec_utils import Option, datetime\n\n",
        ]

        if self.config.generator.objects.fields_literal_types:
            lines.append("from telegrinder.types.enums import *  # noqa: F403\n")

        all_ = ["Model"]
        for object_schema in sorted(self.objects, key=lambda obj: obj.subtypes, reverse=True):
            if object_schema.name != "InputFile":
                lines.append(self.make_object(object_schema) + "\n\n")

            all_.append(object_schema.name)

        lines.append(f"\n__all__ = {tuple(set(all_))!r}\n")

        objects_file = path / "objects.py"
        with open(file=objects_file, mode="w+", encoding="UTF-8") as f:
            f.writelines(lines)

        enums_all = tuple(
            set(
                importlib.import_module(name=(path / "enums").as_posix().replace("/", ".")).__all__,
            ),
        )
        with open(file=path / "__init__.py", mode="w+", encoding="UTF-8") as f:
            f.writelines(
                [
                    "from telegrinder.types.enums import *\n",
                    "from telegrinder.types.objects import *\n\n",
                    f"__all__ = {enums_all + tuple(all_)}\n",
                ],
            )

        logger.info(
            "Generation of {} objects into {} has been completed.",
            len(self.objects),
            objects_file,
        )


class MethodGenerator(ABCGenerator):
    def __init__(
        self,
        methods: list[MethodSchema],
        config: Config,
        parent_types: dict[str, list[str]],
        *,
        release_date: str | None = None,
    ) -> None:
        self.methods = methods
        self.config = config
        self.parent_types = parent_types
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
        /,
    ) -> MethodsParamsLiteralTypesParam | None:
        for p_literal_types in self.config.generator.methods.params_literal_types:
            if method_name == p_literal_types.method_name:
                for param in p_literal_types.params:
                    if param.name == param_name:
                        return param

        return None

    def get_typed_default_param(self, name: str, /) -> TypedDefaultParameter | None:
        name = makesafe_name(name)

        for param in self.config.generator.api.typed_default_parameters:
            if param.name == name:
                return param

        return None

    def make_method_body(self, method_schema: MethodSchema, /) -> str:
        field_descriptions = filter(
            None,
            [
                (
                    f":param {makesafe_name(x.name)}: "
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

    def make_method_params(
        self,
        method_name: str,
        params: list[MethodParameter] | None = None,
    ) -> list[str]:
        if not params:
            return []

        result = []
        for p in (
            *filter(lambda x: x.required and not self.get_typed_default_param(x.name), params),
            *filter(lambda x: not x.required or self.get_typed_default_param(x.name), params),
        ):
            literal_types = self.get_param_literal_types(method_name, p.name)
            param_name = makesafe_name(p.name)

            if literal_types is not None:
                tp = literal_types.enum or "typing.Literal[%s]" % ", ".join(
                    f'"{x}"' if isinstance(x, str) else str(x) for x in literal_types.literals
                )
                p.types = [tp]

            if p.description and is_unixtime_type(param_name, p.types, p.description):
                p.types.insert(p.types.index("Integer"), "Unixtime")

            default_param_value = (
                None if self.get_typed_default_param(param_name) is None else f'default_params["{param_name}"]'
            )
            code = f"{TAB * 2}{param_name}: "

            if not p.required or default_param_value:
                code += (
                    f"{self.make_type_hint(p.types)} {'| None ' if not p.required else ''}= {default_param_value}"
                )
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

    def generate(self, path: pathlib.Path) -> None:
        if not self.methods:
            logger.error("Methods is empty.")
            sys.exit(-1)

        logger.debug("Generate methods...")
        docstring = '    """Telegram Bot API version `{}`, released `{}`."""\n\n'.format(
            self.config.telegram_bot_api.version_number,
            self.release_date or datetime.datetime.now().ctime(),
        )
        default_params_typeddict = 'typing.TypedDict("DefaultParams", {})'.format(
            "{%s}"
            % ", ".join(
                f""""{x.name}": {convert_to_python_type(x.type, parent_types=self.parent_types)}"""
                for x in self.config.generator.api.typed_default_parameters
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
            "    from telegrinder.api.api import API\n    from telegrinder.client.abc import ABCClient\n\n\n",
            "class APIMethods[HTTPClient: ABCClient]:\n" + docstring,
            f"\n\n    default_params = ProxiedDict({default_params_typeddict})\n\n",
            '    def __init__(self, api: "API[HTTPClient]") -> None:\n',
            "        self.api = api\n\n",
        ]

        for method_schema in self.methods:
            lines.append(self.make_method(method_schema) + "\n\n")

        methods_file = path / "methods.py"
        with open(file=methods_file, mode="w+", encoding="UTF-8") as f:
            lines.append('\n\n\n__all__ = ("APIMethods",)\n\n')
            f.writelines(lines)

        logger.info(
            "Generation of {} methods into {} has been completed.",
            len(self.methods),
            methods_file,
        )


def generate(
    *,
    directory: str | pathlib.Path | None = None,
    object_generator: ABCGenerator | None = None,
    method_generator: ABCGenerator | None = None,
) -> None:
    logger.debug("Reading config file...")
    config_toml = read_config(TYPEGEN_DIR / "config.toml")
    config = config_toml.as_model(Config, dec_hook=dec_hook)

    directory = pathlib.Path(directory) if directory else config.generator.directory
    if not os.path.exists(directory):
        logger.warning(f"Directory {directory} not found. Make directory...")
        os.makedirs(directory)

    logger.info(f"Generation... Directory: {directory}")

    schema = download_schema(config_toml, config)
    if object_generator is None or method_generator is None:
        object_generator = object_generator or ObjectGenerator(
            objects=schema.objects,
            config=config,
        )
        method_generator = method_generator or MethodGenerator(
            methods=schema.methods,
            parent_types=(object_generator.parent_types if isinstance(object_generator, ObjectGenerator) else {}),
            config=config,
            release_date=schema.release_date,
        )

    object_generator.generate(directory)
    method_generator.generate(directory)
    logger.info("Successful generation!")

    run_sort_all(directory)
    run_ruff_linter(directory)
    merge_shortcuts(path_api_methods=directory / "methods.py")


__all__ = ("ABCGenerator", "MethodGenerator", "ObjectGenerator", "generate")
