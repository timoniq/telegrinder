import logging
import os
import pathlib
import re
import typing
from collections import OrderedDict
from copy import deepcopy

import requests

URL = "https://ark0f.github.io/tg-bot-api/openapi.json"
TYPES = {
    "integer": "int",
    "string": "str",
    "long": "int",
    "bytes": "bytes",
    "boolean": "bool",
    "number": "float",
    "true": "bool",
    "false": "bool",
}
SPACES = "    "
NS = pathlib.Path("typegen/nicification.py").read_text()


def find_nicifications(name: str) -> list[str]:
    regex = r"class .+\(" + name + r"\):\n((?:.|\n {4}|\n$)+)"
    matches = list(re.finditer(regex, NS, flags=re.MULTILINE))
    if matches:
        return [match.group(1) for match in matches]
    return []


def convert_to_option(func):
    def wrapper(
        obj_name: str,
        param_name: str,
        d: dict,
        obj: dict,
        forward_ref: bool = True,
    ):
        t = func(obj_name, param_name, d, obj, forward_ref)
        if param_name not in obj.get("required", []) and param_name:
            t = "Option[" + t + "]"
        return t

    return wrapper


def chunks_str(s: str) -> str:
    words = s.split(" ")
    s = ""
    line = 0
    for word in words:
        s += word + " "
        line += len(word)
        if line >= 60:
            s += "\n"
            line = 0
    return s


def to_snakecase(s: str) -> str:
    ns = ""
    for i, symbol in enumerate(s):
        if i == 0:
            ns = ns + symbol.lower()
        else:
            ns = ns + (symbol if symbol.islower() else "_" + symbol.lower())
    return ns.replace("__", "_")


def snake_to_pascal(s: str) -> str:
    return "".join(map(str.title, s.split("_")))


@convert_to_option
def convert_type(
    obj_name: str,
    param_name: str,
    d: dict,
    obj: dict,
    forward_ref: bool = True,
) -> str:
    if "type" in d:
        t = d["type"]
        if "enum" in d and obj_name and param_name:
            return obj_name + snake_to_pascal(param_name)
        if t in TYPES:
            return TYPES[t]
        elif t == "array":
            nt = convert_type(obj_name, "", d["items"], obj, forward_ref)
            return "list[" + nt + "]"
        else:
            if "." in t:
                t = t.split(".")[-1]
            return repr(t)
    elif "$ref" in d:
        n = d["$ref"].split("/")[-1]
        if forward_ref:
            return '"' + n + '"'
        return n
    elif "anyOf" in d:
        return (
            "typing.Union["
            + ", ".join(
                convert_type(obj_name, "", ut, obj, forward_ref) for ut in d["anyOf"]
            )
            + "]"
        )
    else:
        logging.error(f"cannot handle {d}")
        return ""


def param_s(obj_name: str, param_name: str, param: dict, obj: dict) -> str:
    t = convert_type(obj_name, param_name, param, obj)
    default_value = param.get("default", None)
    s = "{}: {}{}\n".format(
        param_name if param_name not in ("json", "from") else param_name + "_",
        t,
        " = {}".format(
            "Some({})".format(
                (
                    obj_name
                    + snake_to_pascal(param_name)
                    + "("
                    + repr(default_value)
                    + ")"
                )
                if "enum" in param and default_value is not None
                else repr(default_value)
            )
            if default_value is not None
            else "Nothing",
        )
        if t.startswith("Option")
        else "",
    )
    return s


def properties_ordering(obj: dict) -> dict:
    if not obj.get("required"):
        return obj
    obj = deepcopy(obj)
    ordered_properties = OrderedDict(properties=dict())
    for require in obj["required"]:
        ordered_properties["properties"][require] = obj["properties"].pop(require)
    obj["properties"] = ordered_properties["properties"] | obj["properties"]
    return obj


def get_lines_for_object(name: str, properties: dict, obj: dict):
    if not properties:
        if name == "InputFile":
            return (
                "\n\n"
                + name
                + ' = typing.NamedTuple("InputFile", [("filename", str), ("data", bytes)])\n'
            )
        else:
            print("todo: handle {}".format(name))

    nicifications = find_nicifications(name)
    desc = ""
    if "description" in obj:
        d = obj["description"]
        d = chunks_str(d)
        d = d.replace("\\", "").replace("\n", SPACES + "\n")
        if "externalDocs" in obj:
            d += "\nDocs: {}".format(obj["externalDocs"]["url"])
        desc = SPACES + '"""' + d + '"""\n'

    properties = properties_ordering(obj).get("properties", properties)
    return [
        "\n\n",
        "class {}(Model):\n".format(name),
        desc,
        *(
            [SPACES + "pass\n"]
            if not properties
            else (
                SPACES + param_s(name, pname, param, obj)
                for (pname, param) in properties.items()
                if pname != "flags"
            )
        ),
        *nicifications,
    ]


def get_lines_for_enum(name: str, propert_name: str, propert: dict):
    description = chunks_str(propert.get("description", ""))
    description = description.replace("\\", "").replace("\n", SPACES + "\n")
    description = SPACES + '"""' + description + '"""\n'
    enum_name = name + snake_to_pascal(propert_name)
    return [
        "\n\n",
        "class {}(str, enum.Enum):\n".format(enum_name),
        description,
        *(
            [
                SPACES
                + (
                    x.replace("/", "_").replace("-", "_").strip().upper()
                    + ' = "{}"\n'.format(x)
                )
                for x in propert["enum"]
            ]
        ),
    ]


def parse_response(rt: str):
    if rt.startswith('"'):
        rt = rt[1:-1]
    return f"return full_result(result, {rt})"


def get_ref_names(ref_list: list[dict]) -> typing.List[str]:
    return [d["$ref"].split("/")[-1] for d in ref_list]


def generate(path: str, schema_url: str = URL) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    schema = requests.get(schema_url).json()

    paths = schema["paths"]
    objects = schema["components"]["schemas"]

    with open(path + "/__init__.py", "w", encoding="UTF-8") as file:
        file.writelines(
            [
                "from telegrinder.types.objects import *\n",
                "from telegrinder.types.enums import *\n",
            ]
        )

    with open(path + "/objects.py", "w", encoding="UTF-8") as file:
        file.writelines(
            [
                "import typing\n\n",
                "from telegrinder.option import Nothing, Some\n"
                "from telegrinder.option.msgspec_option import Option\n",
                "from telegrinder.model import *\n",
                "from telegrinder.types.enums import *\n",
            ]
        )

    with open(path + "/enums.py", "w", encoding="UTF-8") as file:
        file.write("import enum\n\n")

    for name, obj in objects.items():
        t, properties = obj.get("type", "object"), obj.get("properties", [])

        with open(path + "/objects.py", "a", encoding="UTF-8") as file:
            if obj.get("anyOf"):
                # creating merge to parse as fast as possible
                ref_names = get_ref_names(obj["anyOf"])
                merged_properties = {}
                for ref_name in ref_names:
                    ref = objects[ref_name]
                    merged_properties.update(ref["properties"])
                properties = merged_properties
            obj_lines = get_lines_for_object(name, properties, obj)
            file.writelines(obj_lines)

        with open(path + "/enums.py", "a", encoding="UTF-8") as file:
            for propert_name in properties:
                if "enum" in properties[propert_name]:
                    file.writelines(
                        get_lines_for_enum(name, propert_name, properties[propert_name])
                    )

    with open(path + "/methods.py", "w", encoding="UTF-8") as file:
        file.writelines(
            [
                "import typing\n",
                "from .objects import *\n",
                "from telegrinder.result import Result\n",
                "from telegrinder.api.error import APIError\n",
                "from telegrinder.option import Nothing\n",
                "from telegrinder.option.msgspec_option import Option\n\n",
                "if typing.TYPE_CHECKING:\n",
                SPACES + "from telegrinder.api.abc import ABCAPI\n\n",
                'X = typing.TypeVar("X")\n',
                'Value = typing.TypeVar("Value")\n',
                "\n\n",
                "class APIMethods:\n",
                SPACES + 'def __init__(self, api: "ABCAPI"):\n',
                SPACES + SPACES + "self.api = api\n",
            ]
        )

    for ps in paths:
        method = paths[ps]
        if "requestBody" not in method["post"]:
            props = {}
        else:
            props = list(method["post"]["requestBody"]["content"].values())[-1][
                "schema"
            ]["properties"]

        lines = []
        method_name = ps[1:]
        fobj = list(method["post"]["responses"]["200"]["content"].values())[-1][
            "schema"
        ]
        result = fobj["properties"]["result"]
        response = convert_type("", "", result, {}, False)
        name = to_snakecase(method_name)
        lines.append(f"async def {name}(\n        self,\n")
        for n, prop in props.items():
            t = convert_type("", "", prop, {}, False)
            lines.append(SPACES + f"{n}: {t} | Option[{t}] | None = None,\n")
        lines.append(SPACES + "**other\n")
        lines.append(f") -> Result[{response}, APIError]:\n")
        lines.extend(
            [
                SPACES + li
                for li in (
                    "result = await self.api.request_raw({}, get_params(locals()))\n".format(
                        '"' + method_name + '"'
                    ),
                    ("\n" + SPACES + SPACES).join(parse_response(response).split("\n"))
                    + "\n",
                )
            ]
        )
        with open(path + "/methods.py", "a", encoding="UTF-8") as file:
            file.writelines(["\n\n"] + [SPACES + li for li in lines])

    print("generated.")

    try:
        print("run black...")
        os.system("black " + path)
    except:  # noqa
        print("cant run black")
