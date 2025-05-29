from __future__ import annotations

import abc
import inspect
from collections import deque
from types import AsyncGeneratorType, CodeType, resolve_bases

import typing_extensions as typing

from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic.function import function_context, get_func_annotations
from telegrinder.tools.strings import to_pascal_case

if typing.TYPE_CHECKING:
    from telegrinder.node.tools.generator import generate_node
else:

    def generate_node(*args, **kwargs):
        from telegrinder.node.tools.generator import generate_node

        return generate_node(*args, **kwargs)


type NodeType = Node | NodeProto[typing.Any]
type IsNode = NodeType | type[NodeType]

T = typing.TypeVar("T", default=typing.Any)

ComposeResult: typing.TypeAlias = T | typing.Awaitable[T] | typing.AsyncGenerator[T, None]

UNWRAPPED_NODE_KEY = "__unwrapped_node__"


@typing.overload
def is_node(maybe_node: type[typing.Any], /) -> typing.TypeIs[type[NodeType]]: ...


@typing.overload
def is_node(maybe_node: typing.Any, /) -> typing.TypeIs[NodeType]: ...


def is_node(maybe_node: typing.Any, /) -> bool:
    if isinstance(maybe_node, typing.TypeAliasType):
        maybe_node = maybe_node.__value__
    if not isinstance(maybe_node, type):
        maybe_node = typing.get_origin(maybe_node) or maybe_node

    return (
        hasattr(maybe_node, "as_node")
        or isinstance(maybe_node, type)
        and issubclass(maybe_node, (Node, NodeProto))
        or not isinstance(maybe_node, type)
        and isinstance(maybe_node, (Node, NodeProto))
    )


@typing.overload
def as_node(maybe_node: type[typing.Any], /) -> type[NodeType]: ...


@typing.overload
def as_node(maybe_node: typing.Any, /) -> NodeType: ...


@typing.overload
def as_node(*maybe_nodes: type[typing.Any]) -> tuple[type[NodeType], ...]: ...


@typing.overload
def as_node(*maybe_nodes: typing.Any) -> tuple[NodeType, ...]: ...


@typing.overload
def as_node(*maybe_nodes: type[typing.Any] | typing.Any) -> tuple[IsNode, ...]: ...


def as_node(*maybe_nodes: typing.Any) -> typing.Any | tuple[typing.Any, ...]:
    for maybe_node in maybe_nodes:
        if not is_node(maybe_node):
            is_type = isinstance(maybe_node, type)
            raise LookupError(
                f"{'Type of' if is_type else 'Object of type'} "
                f"{maybe_node.__name__ if is_type else maybe_node.__class__.__name__!r} "
                "cannot be resolved as Node."
            )
    return maybe_nodes[0] if len(maybe_nodes) == 1 else maybe_nodes


def bind_orig(node: type[NodeType], orig: typing.Any) -> type[NodeType]:
    if issubclass(node, FactoryNode):
        return node
    return type(node.__name__, (node,), {"__orig__": orig})  # type: ignore


@function_context("nodes")
def get_nodes(function: typing.Callable[..., typing.Any], /) -> dict[str, type[NodeType]]:
    return {k: bind_orig(v.as_node(), v) for k, v in get_func_annotations(function).items() if is_node(v)}


@function_context("is_generator")
def is_generator(
    function: typing.Callable[..., typing.Any],
    /,
) -> typing.TypeGuard[AsyncGeneratorType[typing.Any, None]]:
    return inspect.isasyncgenfunction(function)


def unwrap_node(node: type[NodeType], /) -> tuple[type[NodeType], ...]:
    """Unwrap node as flattened tuple of node types in ordering required to calculate given node.

    Provides caching for passed node type.
    """
    if (unwrapped := getattr(node, UNWRAPPED_NODE_KEY, None)) is not None:
        return unwrapped

    stack = deque([(node, node.get_subnodes().values())])
    visited = list[type[NodeType]]()

    while stack:
        parent, child_nodes = stack.pop()

        if parent not in visited:
            visited.insert(0, parent)

        for child in child_nodes:
            stack.append((child, child.get_subnodes().values()))

    unwrapped = tuple(visited)
    setattr(node, UNWRAPPED_NODE_KEY, unwrapped)
    return unwrapped


class ComposeError(BaseException):
    def __init__(self, message: str = "<no error description>", /) -> None:
        self.message = message
        super().__init__(message)


@typing.runtime_checkable
class Composable[R](typing.Protocol):
    @classmethod
    def compose(cls, *args: typing.Any, **kwargs: typing.Any) -> ComposeResult[R]: ...


class NodeImpersonation(typing.Protocol):
    @classmethod
    def as_node(cls) -> type[NodeProto[typing.Any]]: ...


class NodeComposeFunction[R](typing.Protocol):
    __name__: str
    __code__: CodeType

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> ComposeResult[R]: ...


@typing.runtime_checkable
class NodeProto[R](Composable[R], NodeImpersonation, typing.Protocol):
    @classmethod
    def get_subnodes(cls) -> dict[str, type[NodeType]]: ...

    @classmethod
    def is_generator(cls) -> bool: ...


class Node(abc.ABC):
    node: str = "node"
    scope: NodeScope = NodeScope.PER_EVENT

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @classmethod
    def get_subnodes(cls) -> dict[str, type[NodeType]]:
        return get_nodes(cls.compose)

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> bool:
        return is_generator(cls.compose)


class scalar_node[T]:  # noqa: N801
    @typing.overload
    def __new__(cls, x: NodeComposeFunction[Composable[T]], /) -> type[T]: ...

    @typing.overload
    def __new__(cls, x: NodeComposeFunction[T], /) -> type[T]: ...

    @typing.overload
    def __new__(
        cls,
        /,
        *,
        scope: NodeScope,
    ) -> typing.Callable[[NodeComposeFunction[Composable[T]]], type[T]]: ...

    @typing.overload
    def __new__(
        cls,
        /,
        *,
        scope: NodeScope,
    ) -> typing.Callable[[NodeComposeFunction[T]], type[T]]: ...

    def __new__(cls, x=None, /, *, scope=NodeScope.PER_EVENT) -> typing.Any:
        def inner(node_or_func, /) -> typing.Any:
            namespace = {"node": "scalar", "scope": scope, "__module__": node_or_func.__module__}

            if isinstance(node_or_func, type):
                bases: list[type[typing.Any]] = [node_or_func]
                node_bases = resolve_bases(node_or_func.__bases__)
                if not any(issubclass(base, Node) for base in node_bases if isinstance(base, type)):
                    bases.append(Node)
                return type(node_or_func.__name__, tuple(bases), namespace)
            else:
                base_node = generate_node(
                    func=node_or_func,
                    subnodes=tuple(get_nodes(node_or_func).values()),
                )
                return type(to_pascal_case(node_or_func.__name__), (base_node,), namespace)

        return inner if x is None else inner(x)


@typing.dataclass_transform(kw_only_default=True)
class FactoryNode(Node, abc.ABC):
    node = "factory"

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    def __new__(cls, **context: typing.Any) -> type[typing.Self]:
        namespace = dict(**cls.__dict__)
        namespace.pop("__new__", None)
        return type(cls.__name__, (cls,), namespace | context)  # type: ignore


@typing.dataclass_transform()
class DataNode(Node, abc.ABC):
    node = "data"

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult[typing.Self]:
        pass


@scalar_node(scope=NodeScope.PER_CALL)
class Name:
    @classmethod
    def compose(cls) -> str: ...


@scalar_node
class NodeClass:
    @classmethod
    def compose(cls) -> type: ...


class GlobalNode[Value](Node):
    scope = NodeScope.GLOBAL

    @classmethod
    def set(cls, value: Value, /) -> None:
        setattr(cls, "_value", value)

    @typing.overload
    @classmethod
    def get(cls) -> Value: ...

    @typing.overload
    @classmethod
    def get[Default](cls, *, default: Default) -> Value | Default: ...

    @classmethod
    def get(cls, **kwargs: typing.Any) -> typing.Any:
        sentinel = object()
        default = kwargs.pop("default", sentinel)
        return getattr(cls, "_value") if default is sentinel else getattr(cls, "_value", default)

    @classmethod
    def unset(cls) -> None:
        if hasattr(cls, "_value"):
            delattr(cls, "_value")


__all__ = (
    "Composable",
    "ComposeError",
    "DataNode",
    "FactoryNode",
    "GlobalNode",
    "IsNode",
    "Name",
    "Node",
    "NodeImpersonation",
    "NodeProto",
    "NodeType",
    "as_node",
    "get_nodes",
    "is_node",
    "scalar_node",
    "unwrap_node",
    "NodeClass",
)
