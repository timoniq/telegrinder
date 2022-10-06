import logging
import os
import re
import typing
import pathlib

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
NS = pathlib.Path("./nicification.py").read_text()


def find_nicifications(name: str) -> typing.List[str]:
    regex = r"class .+\(" + name + r"\):\n((?:.|\n {4}|\n$)+)"
    matches = list(re.finditer(regex, NS, flags=re.MULTILINE))
    if matches:
        return [match.group(1) for match in matches]
    return []


def convert_optional(func):
    def wrapper(name: str, d: dict, obj: dict, forward_ref: bool = True):
        t = func(name, d, obj, forward_ref)
        if name not in obj.get("required", []) and name:
            t = "typing.Optional[" + t + "]"
        return t

    return wrapper


@convert_optional
def convert_type(name: str, d: dict, obj: dict, forward_ref: bool = True) -> str:
    if "type" in d:
        t = d["type"]
        if t in TYPES:
            return TYPES[t]
        elif t == "array":
            nt = convert_type(name, d["items"], obj, forward_ref)
            return "typing.List[" + nt + "]"
        else:
            if "." in t:
                t = t.split(".")[-1]
            return repr(t)
    elif "$ref" in d:
        n = d["$ref"].split("/")[-1]
        if forward_ref:
            return '"' + n + '"'
        else:
            return n
    elif "anyOf" in d:
        return (
            "typing.Union["
            + ", ".join(convert_type(name, ut, obj, forward_ref) for ut in d["anyOf"])
            + "]"
        )
    else:
        logging.error(f"cannot handle {d}")


def to_snakecase(s: str) -> str:
    ns = ""
    for i, symbol in enumerate(s):
        if i == 0:
            ns = ns + symbol.lower()
        else:
            ns = ns + (symbol if symbol.islower() else "_" + symbol.lower())
    return ns.replace("__", "_")


def param_s(name: str, param: dict, obj: dict) -> str:
    t = convert_type(name, param, obj)
    s = "{}: {}{}\n".format(
        name if name not in ("json", "from") else name + "_",
        t,
        " = " + repr(param.get("default", None))
        if t.startswith("typing.Optional")
        else "",
    )
    return s


def get_lines_for_object(name: str, properties: dict, obj: dict):
    nicifications = find_nicifications(name)

    return [
        "\n\n",
        "class {}(Model):\n".format(name),
        # SPACES + "\"\"\"{}\"\"\"".format(obj["documentation"]),
        *(
            [SPACES + "pass\n"]
            if not properties
            else (
                SPACES + param_s(name, param, obj)
                for (name, param) in properties.items()
                if name != "flags"
            )
        ),
        *nicifications
    ]


def parse_response(rt: str):
    if rt.startswith('"'):
        rt = rt[1:-1]
    return f"return full_result(result, {rt})"


def get_ref_names(ref_list: typing.List[dict]) -> typing.List[str]:
    return [d["$ref"].split("/")[-1] for d in ref_list]


def generate(path: str, schema_url: str = URL) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    schema = requests.get(schema_url).json()

    paths = schema["paths"]
    objects = schema["components"]["schemas"]

    with open(path + "/__init__.py", "w") as file:
        file.writelines("from telegrinder.types.objects import *\n")

    with open(path + "/objects.py", "w") as file:
        file.writelines(["import typing\n", "from telegrinder.model import *\n"])

    for name, obj in objects.items():
        t, properties = obj.get("type", "object"), obj.get("properties", [])

        with open(path + "/objects.py", "a") as file:
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

    # with open(path + "/objects.py", "a") as file:
    #     file.writelines(
    #         [
    #             "\n\n",
    #              "for v in locals().copy().values():\n",
    #             SPACES + "if inspect.isclass(v) and issubclass(v, Model):\n",
    #             SPACES + SPACES + "v.update_forward_refs()",
    #             "\n\n",
    #              "__all__ = (\n",
    #         ]
    #         + [SPACES + repr(n) + ",\n" for n in objects]
    #         + [")\n"]
    #     )

    with open(path + "/methods.py", "w") as file:
        file.writelines(
            [
                "import typing\n",
                "from .objects import *\n",
                "from telegrinder.tools import Result\n",
                "from telegrinder.api.error import APIError\n\n",
                "if typing.TYPE_CHECKING:\n",
                SPACES + "from telegrinder.api.abc import ABCAPI\n\n",
                'X = typing.TypeVar("X")\n',
                "\n\n",
                "class APIMethods:\n",
                SPACES + 'def __init__(self, api: "ABCAPI"):\n',
                SPACES + SPACES + "self.api = api\n\n",
                SPACES + "@staticmethod\n",
                SPACES + "def get_params(loc: dict) -> dict:\n",
                SPACES
                + SPACES
                + 'n = {k: v for k, v in loc.items() if k not in ("self", "other") and v is not None}\n',
                SPACES + SPACES + "n.update(loc['other'])\n        return n\n",
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
        response = convert_type("", result, {}, False)
        name = to_snakecase(method_name)
        lines.append(f"async def {name}(\n        self,\n")
        for n, prop in props.items():
            t = convert_type("", prop, {}, False)
            lines.append(SPACES + f"{n}: typing.Optional[{t}] = None,\n")
        lines.append(SPACES + "**other\n")
        lines.append(f") -> Result[{response}, APIError]:\n")
        lines.extend(
            [
                SPACES + li
                for li in (
                    "result = await self.api.request_raw({}, self.get_params(locals()))\n".format(
                        '"' + method_name + '"'
                    ),
                    ("\n" + SPACES + SPACES).join(parse_response(response).split("\n"))
                    + "\n",
                )
            ]
        )
        with open(path + "/methods.py", "a") as file:
            file.writelines(["\n\n"] + [SPACES + li for li in lines])

    print("generated.")
    try:
        os.system("black ../types")
    except:
        print("cant run black")
