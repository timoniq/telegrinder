import logging
import os
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


def convert_type(d: dict) -> str:
    if "type" in d:
        t = d["type"]
        if t in TYPES:
            return TYPES[t]
        elif t == "array":
            nt = convert_type(d["items"])
            return "typing.List[" + nt + "]"
        else:
            if "." in t:
                t = t.split(".")[-1]
            return repr(t)
    elif "$ref" in d:
        n = d["$ref"].split("/")[-1]
        return repr(n)
    elif "anyOf" in d:
        return "typing.Union[" + ", ".join(convert_type(ut) for ut in d["anyOf"]) + "]"
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


def get_lines_for_object(name: str, properties: dict):
    return [
        "\n\n",
        "class {}(BaseModel):\n".format(name),
        *(
            [SPACES + "pass\n"]
            if not properties
            else (
                SPACES
                + "{}: {}\n".format(
                    name if name not in ("json", "from") else name + "_",
                    "typing.Optional[" + convert_type(param) + "] = None",
                )
                for (name, param) in properties.items()
                if name != "flags"
            )
        ),
    ]


def parse_response(rt: str):
    if rt.startswith("'"):
        return "return Result(True, value=" + rt[1:-1] + "(**self.get_response(u)))"
    elif rt.startswith("typing"):
        if rt.startswith("typing.Union"):
            ts = rt[len("typing.Union")+1:-1].split(", ")
            ts_prim = [t for t in ts if not t.startswith("'")]
            s = ""
            for prim in ts_prim:
                s += f"if isinstance(u, {prim}): return Result(True, value=u)\n"
            comp = [t for t in ts if t not in ts_prim]
            print(comp, ts, ts_prim)
            if len(comp) > 1:
                print("cannot parse", rt)
                exit(0)
            s += "return Result(True, value=" + comp[0][1:-1] + "(**self.get_response(u)))"
            return s
        elif rt.startswith("typing.List"):
            n = rt[len("typing.List")+1:-1]
            if not n.startswith("'"):
                print("no instruction to parse list of", n)
                exit(0)
            return f"return Result(True, value=[{n[1:-1]}(**self.get_response(e)) for e in u])"
    return "return Result(True, value=u)"


def generate(path: str, schema_url: str = URL) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

    schema = requests.get(schema_url).json()

    paths = schema["paths"]
    objects = schema["components"]["schemas"]

    with open(path + "/__init__.py", "w") as file:
        file.writelines("from telegrinder.types.objects import *\n")

    with open(path + "/objects.py", "w") as file:
        file.writelines(
            ["import typing\n", "import inspect\n", "from telegrinder.tbase import *\n"]
        )

    for name, obj in objects.items():
        t, properties = obj.get("type", "object"), obj.get("properties", [])

        with open(path + "/objects.py", "a") as file:
            file.writelines(get_lines_for_object(name, properties))

    with open(path + "/objects.py", "a") as file:
        file.writelines(
            [
                "\n\n",
                "for v in locals().copy().values():\n",
                SPACES + "if inspect.isclass(v) and issubclass(v, BaseModel):\n",
                SPACES + SPACES + "v.update_forward_refs()",
                "\n\n",
                "__all__ = (\n",
            ]
            + [SPACES + repr(n) + ",\n" for n in objects]
            + [")\n"]
        )

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
                SPACES + SPACES + "n.update(loc['other'])\n        return n\n\n",
                SPACES + "@staticmethod\n",
                SPACES + "def get_response(r: dict) -> dict:\n",
                SPACES + SPACES + "if 'json' in r: r['json_'] = r['json']\n",
                SPACES + SPACES + "return r",
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
        result = list(method["post"]["responses"]["200"]["content"].values())[-1][
            "schema"
        ]["properties"]["result"]
        response = convert_type(result)
        print(response)
        name = to_snakecase(method_name)
        lines.append(f"async def {name}(\n        self,\n")
        for n, prop in props.items():
            t = convert_type(prop)
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
                    SPACES + "u = result.unwrap()\n",
                    SPACES + ("\n" + SPACES + SPACES + SPACES).join(parse_response(response).split("\n")) + "\n",
                    "return Result(False, error=result.error)",
                )
            ]
        )
        with open(path + "/methods.py", "a") as file:
            file.writelines(["\n\n"] + [SPACES + li for li in lines])
