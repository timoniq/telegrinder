import os
import requests

URL = "https://core.telegram.org/schema/json"
TYPES = {
    "int": "int",
    "string": "str",
    "long": "int",
    "bytes": "bytes",
    "Bool": "bool",
    "double": "float",
    "true": "bool",
    "false": "bool",
}
SPACES = "    "


def convert_type(t: str) -> str:
    if "?" in t:
        t = t.split("?")[-1]
    if t == "!X":
        return "X"
    if t == "#":
        return "typing.List[str]"
    if t in TYPES:
        return TYPES[t]
    elif t.startswith("Vector"):
        nt = t[7:-1]
        return "typing.List[" + convert_type(nt) + "]"
    else:
        if "." in t:
            t = t.split(".")[-1]
        return repr(t)


def to_snakecase(s: str) -> str:
    ns = ""
    for i, symbol in enumerate(s):
        if i == 0:
            ns = ns + symbol.lower()
        else:
            ns = ns + (symbol if symbol.islower() else "_" + symbol.lower())
    return ns.replace("__", "_")


def generate(path: str, schema_url: str = URL) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    schema = requests.get(schema_url).json()
    methods = schema["methods"]
    constructors = schema["constructors"]
    names = {}

    with open(path + "/__init__.py", "w") as file:
        file.writelines("from telegrinder.types.constructors import *\n")

    for constructor in constructors:
        if constructor["type"] in ("Bool", "True", "Vector t", "Null", "Error"):
            continue
        constructor["type"] = constructor["type"].split(".")[-1]
        if constructor["type"] in names:
            for p in constructor["params"]:
                if p["name"] not in (a["name"] for a in names[constructor["type"]]):
                    names[constructor["type"]].append(p)
        else:
            names[constructor["type"]] = constructor["params"]

    with open(path + "/constructors.py", "w") as file:
        file.writelines(
            ["import typing\n", "import inspect\n", "from pydantic import BaseModel\n"]
        )
    for (name, params) in names.items():
        with open(path + "/constructors.py", "a") as file:
            file.writelines(
                [
                    "\n\n",
                    "class {}(BaseModel):\n".format(name),
                    *(
                        [SPACES + "pass\n"]
                        if not params
                        else (
                            SPACES
                            + "{}: {}\n".format(
                                param["name"]
                                if param["name"] not in ("json",)
                                else param["name"] + "_",
                                "typing.Optional["
                                + convert_type(param["type"])
                                + "] = None",
                            )
                            for param in params
                            if param["name"] != "flags"
                        )
                    ),
                ]
            )

    with open(path + "/constructors.py", "a") as file:
        file.writelines(
            [
                "\n\n",
                "for v in locals().copy().values():\n",
                SPACES + "if inspect.isclass(v) and issubclass(v, BaseModel):\n",
                SPACES + SPACES + "v.update_forward_refs()",
                "\n\n",
                "__all__ = (\n",
            ]
            + [SPACES + repr(n) + ",\n" for n in names]
            + [")\n"]
        )

    with open(path + "/methods.py", "w") as file:
        file.writelines(
            [
                "import typing\n",
                "from .constructors import *\n",
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
                SPACES + SPACES + "n.update(loc['other'])\n        return n\n\n",
                SPACES + "@staticmethod\n",
                SPACES + "def get_response(r: dict) -> dict:\n",
                SPACES + SPACES + "if 'json' in r: r['json_'] = r['json']\n",
                SPACES + SPACES + "return r",
            ]
        )

    for method in methods:
        lines = []
        method_name = method["method"].split(".")[-1]
        name = to_snakecase(method_name)
        params = method["params"]
        response = convert_type(method["type"])
        lines.append(f"async def {name}(\n        self,\n")
        for param in params:
            n = param["name"]
            t = convert_type(param["type"])
            lines.append(SPACES + f"{n}: typing.Optional[{t}] = None,\n")
        lines.append(SPACES + "**other\n")
        lines.append(f") -> Result[{response}, APIError]:\n")
        lines.extend(
            [
                SPACES + li
                for li in (
                    "result = await self.api.request({}, self.get_params(locals()))\n".format(
                        '"' + method_name + '"'
                    ),
                    "if result.is_ok:\n",
                    SPACES
                    + "return Result(True, value="
                    + (
                        response[1:-1] + "(**self.get_response(result.unwrap()))"
                        if response.startswith("'")
                        else "result.unwrap()"
                    )
                    + ")\n",
                    "return Result(False, error=result.error)",
                )
            ]
        )
        with open(path + "/methods.py", "a") as file:
            file.writelines(["\n\n"] + [SPACES + li for li in lines])
