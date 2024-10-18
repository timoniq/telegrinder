import dataclasses
import os
import pathlib
import re
import typing
from collections import OrderedDict

import libcst as cst

from telegrinder.modules import logger

APIMethodsMapping: typing.TypeAlias = dict[str, cst.FunctionDef]

ANNOTATION_TYPING_ANY: typing.Final[cst.Annotation] = cst.parse_statement("x: typing.Any").body[0].annotation  # type: ignore
DEFAULT_API_METHODS_CLASS_NAME: typing.Final[str] = "APIMethods"
DEFAULT_PATH_CUTE_TYPES: typing.Final[pathlib.Path] = pathlib.Path("telegrinder") / "bot" / "cute_types"
DEFAULT_PATH_API_METHODS: typing.Final[pathlib.Path] = pathlib.Path("telegrinder") / "types" / "methods.py"


def is_cute_class(node: cst.ClassDef) -> bool:
    if not node.bases or not (node.name.value != "BaseCute" and node.name.value.endswith("Cute")):
        return False

    # Find the base class with the name "BaseCute" or subscriptable (generic) "BaseCute[...]"
    for base in node.bases:
        if isinstance(base.value, cst.Name) and base.value.value == "BaseCute":
            return True
        if (
            isinstance(base.value, cst.Subscript)
            and isinstance(base.value.value, cst.Name)
            and base.value.value == "BaseCute"
        ):
            return True

    return False


def get_params(node: cst.FunctionDef) -> dict[str, cst.Param]:
    params_dct = OrderedDict()
    optional_params = list(node.params.params)[-sum(1 for x in node.params.params if x.default is not None) :]
    required_params = [param for param in list(node.params.params)[1 : -len(optional_params)]]

    for param in required_params + optional_params:
        params_dct[param.name.value] = param

    return params_dct


def parse_docstring(docstring: str) -> tuple[str, dict[str, str]]:
    docstring_match = re.match(r"(.*?):param\s+(.*)", docstring, re.DOTALL | re.MULTILINE)
    assert docstring_match
    docstring_match = docstring_match.group(1).strip()
    matches = re.findall(r":param\s+(.*?):(.*)", docstring, re.DOTALL)
    return (docstring_match, {m[0].strip(): m[1].strip() for m in matches})


def prepare_docstring(
    shortcut_func: cst.FunctionDef,
    api_method_func: cst.FunctionDef,
    custom_params: set[str],
) -> str | None:
    if shortcut_func.get_docstring() and (api_m_doc := api_method_func.get_docstring()):
        shortcut_docstring_params = {}
        api_method_docstring, api_method_docstring_params = parse_docstring(api_m_doc)
        shortcut_docstring_s = re.sub(
            r"^Method `.+`",
            f"Shortcut `API.{api_method_func.name.value}()`",
            api_method_docstring,
        )

        for param, docstring in api_method_docstring_params.items():
            if param in custom_params:
                continue
            shortcut_docstring_params[param] = docstring

        for param, docstring in shortcut_docstring_params.items():
            docstring = docstring.replace("         ", "")
            shortcut_docstring_s += f"\n:param {param}: {docstring}"

        return '"""{}"""'.format(shortcut_docstring_s)

    return None


def merge(
    path_api_methods: str | pathlib.Path | None = None,
    path_cute_types: str | pathlib.Path | None = None,
    api_methods_class_name: str | None = None,
) -> None:
    path_api_methods = pathlib.Path(path_api_methods or DEFAULT_PATH_API_METHODS)
    path_cute_types = pathlib.Path(path_cute_types or DEFAULT_PATH_CUTE_TYPES)
    api_methods_class_name = api_methods_class_name or DEFAULT_API_METHODS_CLASS_NAME

    logger.info("Merge shortcuts with API methods...")

    api_methods_source_tree = cst.parse_module(path_api_methods.read_text(encoding="UTF-8"))
    api_methods_visitor = APIMethodsCollector(api_methods_class_name)
    api_methods_source_tree.visit(api_methods_visitor)

    for path in path_cute_types.rglob("*.py"):
        logger.info("Parsing module {!r}...", path.name)
        cute_source_tree = cst.parse_module(path.read_text(encoding="UTF-8"))

        shortcuts_visitor = ShortcutsCollector(api_methods_visitor.api_methods)
        cute_source_tree.visit(shortcuts_visitor)

        transformer = ShortcutsCompatibilityTransformer(
            shortcuts_visitor.shortcuts,
            api_methods_visitor.api_methods,
        )
        modified_cute_tree = cute_source_tree.visit(transformer)
        modified_cute_tree_code = modified_cute_tree.code

        if cute_source_tree.code != modified_cute_tree_code:
            print("Rewritting file '{}'...".format(path))
            path.write_text(modified_cute_tree_code, encoding="UTF-8")

    os.system("ruff format {}".format(path_cute_types))


@dataclasses.dataclass(slots=True, eq=False)
class Shortcut:
    function: cst.FunctionDef
    docstring: str | None = dataclasses.field(default=None, kw_only=True)
    method_name: str = dataclasses.field(kw_only=True)
    custom_params: set[str] = dataclasses.field(default_factory=lambda: set(), kw_only=True)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, cst.FunctionDef) and self.function == value


class ShortcutsCollector(cst.CSTVisitor):
    def __init__(self, api_methods: APIMethodsMapping) -> None:
        self.api_methods = api_methods
        self.shortcuts: list[Shortcut] = []

    def visit_ClassDef_body(self, node: cst.ClassDef) -> bool | None:
        """Visit the definition of a class that inherits the `BaseCute` class and the name ends with `Cute`."""

        return is_cute_class(node)

    def visit_FunctionDef_asynchronous(self, node: cst.FunctionDef) -> bool | None:
        """Visit the definition of an async function that are decorated with the `shortcut` decorator."""

        found = False
        for decorator in node.decorators:
            if (
                isinstance(decorator.decorator, cst.Call)
                and isinstance(decorator.decorator.func, cst.Name)
                and decorator.decorator.func.value == "shortcut"
            ):
                kwargs = {}
                for arg in decorator.decorator.args:
                    if isinstance(arg.value, cst.SimpleString):
                        kwargs["method_name"] = arg.value.value.removeprefix('"').removesuffix('"')
                    elif isinstance(arg.value, cst.Set):
                        kwargs["custom_params"] = {
                            e.value.value.removeprefix('"').removesuffix('"')
                            for e in arg.value.elements
                            if isinstance(e.value, cst.SimpleString)
                        }

                self.shortcuts.append(
                    Shortcut(
                        node,
                        docstring=prepare_docstring(
                            node,
                            self.api_methods[kwargs["method_name"]],
                            kwargs.get("custom_params", set()),
                        ),
                        **kwargs,
                    ),
                )
                found = True

        return found


class APIMethodsCollector(cst.CSTVisitor):
    def __init__(self, api_class_methods_name: str) -> None:
        self.api_class_methods_name = api_class_methods_name
        self.api_methods: APIMethodsMapping = {}

    def visit_ClassDef_body(self, node: cst.ClassDef) -> bool | None:
        """Visit the definition of a class that the name == `self.api_class_methods_name` and find definitions of an async function."""

        if node.name.value != self.api_class_methods_name:
            return False

        for statement in node.body.body:
            if isinstance(statement, cst.FunctionDef) and statement.asynchronous is not None:
                self.api_methods[statement.name.value] = statement

        return True


class ShortcutsCompatibilityTransformer(cst.CSTTransformer):
    def __init__(self, shortcuts: list[Shortcut], api_methods: APIMethodsMapping) -> None:
        self.shortcuts = shortcuts
        self.api_methods = api_methods

    def visit_ClassDef_body(self, node: cst.ClassDef) -> bool | None:
        return is_cute_class(node)

    def visit_FunctionDef_asynchronous(self, node: cst.FunctionDef) -> bool | None:
        return node in self.shortcuts

    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef,
    ) -> cst.FunctionDef:
        if typing.cast(Shortcut, original_node) in self.shortcuts:
            shortcut = self.shortcuts.pop(self.shortcuts.index(typing.cast(Shortcut, original_node)))
            shortcut_params = OrderedDict({"self": cst.Param(cst.Name("self"))}) | get_params(
                shortcut.function
            )
            api_method_params = get_params(self.api_methods[shortcut.method_name])

            for name, param in api_method_params.items():
                if name in shortcut.custom_params or param.annotation is None:
                    continue
                if param.default is not None and not isinstance(param.default, cst.Name):
                    continue
                shortcut_params[name] = param

            return updated_node.with_changes(
                params=cst.Parameters(
                    sorted(list(shortcut_params.values()), key=lambda x: x.default is not None),
                    star_kwarg=cst.Param(
                        cst.Name("other"),
                        annotation=ANNOTATION_TYPING_ANY,
                        comma=cst.Comma(cst.TrailingWhitespace()),  # type: ignore
                    ),
                ),
            )

        return updated_node

    def leave_SimpleString(
        self,
        original_node: cst.SimpleString,
        updated_node: cst.SimpleString,
    ) -> cst.SimpleString:
        for shortcut in self.shortcuts:
            if (
                shortcut.docstring
                and shortcut.function.get_docstring(clean=False) == original_node.evaluated_value
            ):
                return updated_node.with_changes(value=shortcut.docstring)

        return updated_node


if __name__ == "__main__":
    merge()


__all__ = ("merge",)
