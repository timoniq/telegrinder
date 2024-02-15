import logging
import os
import re
import sys
import typing
from abc import ABC, abstractmethod

import msgspec
import requests
from models import Field, MethodSchema, Schema, TypeSchema

ModelT = typing.TypeVar("ModelT", bound=msgspec.structs.Struct)

JSON_DECODER: typing.Final[msgspec.json.Decoder] = msgspec.json.Decoder(strict=True)
URL: typing.Final[str] = "https://raw.githubusercontent.com/PaulSonOfLars/telegram-bot-api-spec/main/api.json"
TAB: typing.Final[str] = "    "
TYPES: typing.Final[dict[str, str]] = {
    "String": "str",
    "Integer": "int",
    "Float": "float",
    "Boolean": "bool",
}
MAIN_DIR: typing.Final[str] = "typegen"

logger = logging.getLogger("telegrinder_typegen")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter(
        "{levelname: <8} | {asctime} {funcName}:{lineno} - {message}", style="{"
    )
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_schema_json() -> "SchemaJson":
    logger.debug(f"Requesting {URL!r} to retrieve the schema...")
    raw = requests.get(URL).text
    logger.debug("Schema successfully received! Decoding...")
    dct: dict = JSON_DECODER.decode(raw)
    dct["methods"] = [d for d in dct["methods"].values()]
    dct["types"] = [d for d in dct["types"].values()]
    logger.debug(f"Schema {dct['version']!r} successfully decoded!")
    return dct  # type: ignore


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


def convert_to_python_type(
    tp: str, parent_types: dict[str, list[str]] | None = None
) -> str:
    if tp.startswith("Array of"):
        return f'list[{convert_to_python_type(tp.removeprefix("Array of "), parent_types)}]'
    parent_types = parent_types or {}
    return TYPES.get(
        tp,
        f'"{tp}"'
        if tp not in parent_types
        else "Variative[%s]" % ", ".join(f'"{x}"' for x in parent_types[tp]),
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


def read_enum_ref_config(path: str | None = None) -> dict:
    path = path or MAIN_DIR + "/enum_ref_config.json"
    with open(path, mode="r", encoding="UTF-8") as f:
        return JSON_DECODER.decode(f.read())


class SchemaJson(typing.TypedDict, total=True):
    version: str
    release_date: str
    changelog: str
    methods: typing.NotRequired[list[dict[str, typing.Any]]]
    types: typing.NotRequired[list[dict[str, typing.Any]]]


class RefFields(typing.TypedDict):
    """Mapping containing field name and their reference to enumeration."""

    field_name: str
    """Field name."""

    reference: str
    """Reference to enumeration."""


class EnumRefConfig(typing.TypedDict):
    """References to enumerations in object fields."""

    object_name: str
    """Object name."""

    reference_fields: list[RefFields]
    """Reference fields."""


class ABCGenerator(ABC):
    @abstractmethod
    def generate(self, path: str) -> None:
        pass


class TypesGenerator(ABCGenerator):
    def __init__(
        self,
        types: list[TypeSchema],
        nicification_path: str,
        enum_ref_configs: list[EnumRefConfig] | None = None,
    ) -> None:
        self.types = types
        self.rename_field_names = {
            "from": "from_",
        }
        self.nicification_path = nicification_path
        self.enum_ref_configs = enum_ref_configs or []
        self.parent_types: dict[str, list[str]] = {}

    def get_enum_ref(self, object_name: str, field_name: str) -> str | None:
        for cfg in self.enum_ref_configs:
            if cfg["object_name"] == object_name:
                for ref_field in cfg["reference_fields"]:
                    if ref_field["field_name"] == field_name:
                        return ref_field["reference"]
        return None

    def make_field_type(self, field: Field, enum_ref: str | None = None) -> str:
        code = f"{self.rename_field_names.get(field.name, field.name)}: "

        if enum_ref is not None:
            union_types = (
                f"list[{enum_ref}]"
                if any("Array of" in x for x in field.types)
                else enum_ref
            )
        elif len(field.types) > 1:
            union_types = "Variative[%s]" % ", ".join(
                convert_to_python_type(tp)
                if tp not in self.parent_types
                else "Variative[%s]" % ", ".join(f'"{p}"' for p in self.parent_types[tp])
                for tp in field.types
            )
        else:
            tp = field.types[0]
            union_types = (
                convert_to_python_type(tp)
                if tp not in self.parent_types
                else "Variative[%s]" % ", ".join(f'"{p}"' for p in self.parent_types[tp])
            )

        if not field.required:
            union_types = f"Option[{union_types}] = Nothing"

        code += union_types
        if field.description:
            description = field.description.replace('"', "`")
            sep = "\n" + TAB
            code += f'{sep}"""{chunks_str(description, sep=sep)}"""\n'

        return code

    def make_subtype_of(self, subtype_of: list[str] | None = None) -> str:
        if not subtype_of:
            return "Model"
        return ", ".join(subtype_of)

    def make_type(self, tp_schema: TypeSchema) -> str:
        object_name = camel_to_pascal(tp_schema.name)
        base, nicifications = find_nicifications(object_name, self.nicification_path)
        code = (
            f"class {camel_to_pascal(tp_schema.name)}"
            f"({base if base and base != object_name else self.make_subtype_of(tp_schema.subtype_of)}):\n{TAB}"
        )
        
        if tp_schema.description:
            description = (
                f"Object `{object_name}`, see the [documentation]({tp_schema.href})"
            )
            code += '"""%s\n\n%s\n"""' % (
                description,
                "\n".join(tp_schema.description),
            )

        code += f"\n"
        if not tp_schema.fields and not nicifications:
            if (not tp_schema.subtypes and base is None) or not tp_schema.subtypes:
                logger.warning(
                    f"Object {object_name!r} has not fields, subtypes and nicifications! :("
                )
            else:
                self.parent_types[object_name] = tp_schema.subtypes
            code += f"{TAB}pass"
            return code

        if tp_schema.fields:
            code += TAB
            for f in (
                *filter(lambda f: f.required, tp_schema.fields),
                *filter(lambda f: not f.required, tp_schema.fields),
            ):
                enum_ref = self.get_enum_ref(object_name, f.name)
                code += f"\n{TAB}" + self.make_field_type(f, enum_ref)

        if nicifications:
            n = nicifications[0]
            if tp_schema.fields:
                for f, t, d in re.findall(
                    r'(\b\w+\b):\s*(.+)\s*"""(.*?)"""', n, flags=re.DOTALL
                ):
                    new_code = f'\n    {f}: {t.strip()}\n    """{d}"""'
                    code = re.sub(
                        r"\n    " + f + r": .+((?:.|\n {4}|\n$)+)", new_code, code
                    )
                    n = n.replace(new_code.strip(), "")
            code += n

        return code

    def generate(self, path: str):
        if not self.types:
            logger.error("Types is empty!")
            exit(-1)

        logger.debug(f"Generation of {len(self.types)} objects...")
        lines = [
            "import typing\n\n",
            "from fntypes.variative import Variative\n",
            "from telegrinder.model import Model\n",
            "from telegrinder.msgspec_utils import Option, Nothing\n\n",
        ]

        if self.enum_ref_configs:
            lines.append("from telegrinder.types.enums import *  # noqa\n")

        for type_schema in sorted(self.types, key=lambda x: x.subtypes or [], reverse=True):
            lines.append(self.make_type(type_schema) + "\n\n")

        with open(path + "/objects.py", mode="w", encoding="UTF-8") as f:
            f.writelines(lines)

        logger.debug(
            f"Successful generation of {len(self.types)} objects into {path + '/objects.py'!r}!"
        )


class MethodsGenerator(ABCGenerator):
    def __init__(
        self, methods: list[MethodSchema], parent_types: dict[str, list[str]]
    ) -> None:
        self.methods = methods
        self.parent_types = parent_types

    @staticmethod
    def make_type_hint(
        types: list[str],
        parent_types: dict[str, list[str]] | None = None,
        is_return_type: bool = False,
    ) -> str:
        if not types:
            return "typing.Any"
        sep = ", " if is_return_type else " | "
        return (
            convert_to_python_type(types[0], parent_types).replace('"', "")
            if len(types) == 1
            else ("Variative[%s]" if is_return_type else "%s") % sep.join(
                convert_to_python_type(tp, parent_types).replace('"', "")
                for tp in types
            )
        )

    def make_method_body(self, method_schema: MethodSchema) -> str:
        field_descriptions = filter(
            None,
            [
                f":param {x.name}: " + chunks_str(x.description, sep="\\\n" + TAB + TAB).replace('"', "`")
                if x.description
                else ""
                for x in method_schema.fields or []
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
            + '{}method_response = await self.api.request_raw("{}", get_params(locals()))\n'.format(
                TAB * 2,
                method_schema.name,
            )
            + f"{TAB * 2}return full_result(method_response, "
            + f"{self.make_type_hint(method_schema.returns or [], self.parent_types, is_return_type=True)})"
        )

    def make_method_params(self, params: list[Field] | None = None) -> list[str]:
        result = []
        if not params:
            return result

        for p in (
            *filter(lambda x: x.required, params),
            *filter(lambda x: not x.required, params),
        ):
            code = f"{TAB * 2}{p.name}: "
            if not p.required:
                type_hint = self.make_type_hint(p.types)
                code += f"{type_hint} | Option[{type_hint}] = Nothing"
            else:
                code += self.make_type_hint(p.types)
            result.append(code)

        return result

    def make_return_type(self, returns: list[str] | None = None) -> str:
        if not returns:
            return 'Result[bool, "APIError"]'
        return f'Result[{self.make_type_hint(returns, self.parent_types, is_return_type=True)}, "APIError"]'

    def make_method(self, method_schema: MethodSchema) -> str:
        code = (
            f"{TAB}async def {camel_to_snake(method_schema.name)}(self,"
            + ",\n".join(self.make_method_params(method_schema.fields))
            + ("," if method_schema.fields else "")
            + f"**other: typing.Any{',' if method_schema.fields else ''}) -> "
            + self.make_return_type(method_schema.returns)
            + f":\n{TAB * 2}"
            + self.make_method_body(method_schema)
        )
        return code

    def generate(self, path: str) -> None:
        if not self.methods:
            logger.error("Methods is empty!")
            exit(-1)

        logger.debug(f"Generation of {len(self.methods)} methods...")
        lines = [
            "import typing\n\n",
            "from fntypes.co import Result, Variative\n"
            "from telegrinder.api.error import APIError\n",
            "from telegrinder.msgspec_utils import Option, Nothing\n",
            "from telegrinder.model import full_result, get_params\n",
            "from telegrinder.types.objects import *  # noqa\n\n",
            "if typing.TYPE_CHECKING:\n",
            "    from telegrinder.api.abc import ABCAPI\n\n\n",
            "class APIMethods:\n",
            '    def __init__(self, api: "ABCAPI") -> None:\n',
            "        self.api = api\n\n",
        ]

        for method_schema in self.methods:
            lines.append(self.make_method(method_schema) + "\n\n")

        with open(path + "/methods.py", mode="w", encoding="UTF-8") as f:
            f.writelines(lines)

        logger.debug(
            f"Successful generation of {len(self.methods)} methods into {path + '/methods.py'!r}!"
        )


def generate(
    path: str | None = None,
    enum_ref_cfg_path: str | None = None,
    types_generator: ABCGenerator | None = None,
    methods_generator: ABCGenerator | None = None,
) -> None:
    path = path or "telegrinder/types"
    if not os.path.exists(path):
        logger.warning(f"Path dir {path!r} not found! Making dir...")
        os.makedirs(path)

    if not types_generator or not methods_generator:
        schema = convert_schema_to_model(get_schema_json(), Schema)
        enum_ref_cfg = read_enum_ref_config(enum_ref_cfg_path)
        types_generator = types_generator or TypesGenerator(
            schema.types,
            MAIN_DIR + "/nicifications.py",
            enum_ref_cfg["objects"],  # type: ignore
        )
        methods_generator = methods_generator or MethodsGenerator(
            schema.methods,
            types_generator.parent_types
            if isinstance(types_generator, TypesGenerator)
            else {},
        )

    types_generator.generate(path)
    methods_generator.generate(path)

    logger.debug("Run black formatter...")
    if os.system(f"black {path}") != 0:
        logger.debug("Black formatter failed!")
    else:
        logger.debug("Black formatter successfully formatted files.")
    
    logger.debug("Run isort...")
    if os.system(f"isort {path}") != 0:
        logger.debug("isort failed!")
    else:
        logger.debug("isort successfully sorted imports.")
    
    logger.debug("Schema has been successfully generated.")


__all__ = (
    "ABCGenerator",
    "EnumRefConfig",
    "MethodsGenerator",
    "RefFields",
    "SchemaJson",
    "TypesGenerator",
    "convert_schema_to_model",
    "find_nicifications",
    "generate",
    "get_schema_json",
    "read_enum_ref_config",
)
