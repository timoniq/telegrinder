from __future__ import annotations

import abc
import inspect
from collections import deque
from functools import reduce
from itertools import islice
from types import CodeType, NoneType, UnionType, resolve_bases

import typing_extensions as typing

from telegrinder.node.context import NODE_CONTEXT
from telegrinder.node.exceptions import ComposeError
from telegrinder.node.scope import NodeScope
from telegrinder.node.session import NodeSession
from telegrinder.tools.aio import Generator
from telegrinder.tools.fullname import fullname
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
type AnyNode = IsNode | NodeConvertable

T = typing.TypeVar("T", default=typing.Any)

ComposeResult: typing.TypeAlias = T | typing.Awaitable[T] | Generator[T, typing.Any, typing.Any]

_NODEFAULT = object()
_NONES = {None, NoneType}
_UNION_TYPES = {typing.Union, UnionType}
UNWRAPPED_NODE_KEY: typing.Final[str] = "__unwrapped_node__"


def is_node(maybe_node: typing.Any, /) -> typing.TypeIs[AnyNode]:
    return hasattr(maybe_node, "as_node") or is_node_type(maybe_node)


@typing.overload
def as_node(maybe_node: typing.Any, /) -> IsNode: ...


@typing.overload
def as_node(
    maybe_node: typing.Any,
    /,
    *,
    raise_exception: typing.Literal[False],
) -> IsNode | None: ...


def union_as_node(union: UnionType, /) -> IsNode | None:
    from telegrinder.node.either import _Either

    args = typing.get_args(union)
    if not args:
        return None

    plain, opt = [t for t in args if t not in _NONES], any(t in _NONES for t in args)
    if not plain:
        return None

    nodes: tuple[IsNode, ...] | None = as_node(*plain, raise_exception=False)
    if nodes is None:
        return None

    nodes = (nodes,) if not isinstance(nodes, tuple) else nodes
    node = reduce(
        lambda left, right: _Either[left, right],
        islice(nodes, 1, None),
        nodes[0],  # type: ignore
    )
    return _Either[node] if opt else node


@typing.overload
def as_node(*maybe_nodes: typing.Any) -> tuple[IsNode, ...]: ...


@typing.overload
def as_node(
    *maybe_nodes: typing.Any,
    raise_exception: typing.Literal[False],
) -> tuple[IsNode, ...] | None: ...


def as_node(
    *maybe_nodes: typing.Any,
    raise_exception: bool = True,
) -> IsNode | tuple[IsNode, ...] | None:
    nodes = []

    for maybe_node in maybe_nodes:
        if isinstance(maybe_node, typing.TypeAliasType):
            maybe_node = maybe_node.__value__

        if (typing.get_origin(maybe_node) or maybe_node) in _UNION_TYPES and (
            maybe_node := union_as_node(union := maybe_node)
        ) is None:
            if not raise_exception:
                return None
            raise TypeError(f"Union `{union!r}` doesn't contain all types of Node.")

        if not is_node_type(orig := typing.get_origin(maybe_node) or maybe_node):
            if not hasattr(orig, "as_node"):
                if not raise_exception:
                    return None

                raise TypeError(
                    f"{'Type of' if isinstance(maybe_node, type) else 'Object of type'} "
                    f"{fullname(maybe_node)!r} cannot be resolved as Node.",
                )

            maybe_node = orig.as_node()

        nodes.append(maybe_node)

    return nodes[0] if len(nodes) == 1 else tuple(nodes)


def is_node_type(obj: typing.Any, /) -> typing.TypeIs[IsNode]:
    return isinstance(obj, Node | NodeProto) or (isinstance(obj, type) and issubclass(obj, Node | NodeProto))


@function_context("nodes")
def get_nodes(
    function: typing.Callable[..., typing.Any],
    /,
    *,
    start_idx: int = 0,
) -> dict[str, IsNode]:
    return {
        k: node
        for index, (k, v) in enumerate(get_func_annotations(function).items())
        if (node := as_node(v, raise_exception=False)) is not None and index >= start_idx
    }


@function_context("is_generator")
def is_generator(
    function: typing.Callable[..., typing.Any],
    /,
) -> typing.TypeGuard[Generator[typing.Any, typing.Any, typing.Any]]:
    return inspect.isgeneratorfunction(function) or inspect.isasyncgenfunction(function)


def unwrap_node(node: IsNode, /) -> tuple[IsNode, ...]:
    """Unwrap node as flattened tuple of node types in ordering required to calculate given node.

    Provides caching for passed node type.
    """
    if (unwrapped := getattr(node, UNWRAPPED_NODE_KEY, None)) is not None:
        return unwrapped

    stack = deque([(node, node.get_subnodes().values())])
    visited = list[IsNode]()

    while stack:
        parent, child_nodes = stack.pop()

        if parent not in visited:
            visited.insert(0, parent)

        for child in child_nodes:
            stack.append((child, child.get_subnodes().values()))

    unwrapped = tuple(visited)
    setattr(node, UNWRAPPED_NODE_KEY, unwrapped)
    return unwrapped


@typing.runtime_checkable
class Composable[R](typing.Protocol):
    @classmethod
    def compose(cls, *args: typing.Any, **kwargs: typing.Any) -> ComposeResult[R]: ...


class NodeConvertable(typing.Protocol):
    @classmethod
    def as_node(cls) -> type[NodeProto[typing.Any]]: ...


class NodeComposeFunction[R](typing.Protocol):
    __name__: str
    __code__: CodeType

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> ComposeResult[R]: ...


@typing.runtime_checkable
class NodeProto[R](Composable[R], typing.Protocol):
    @classmethod
    def get_subnodes(cls) -> dict[str, IsNode]: ...

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
    def get_subnodes(cls) -> dict[str, IsNode]:
        return get_nodes(cls.compose)

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

    def __new__(cls, x=None, /, *, scope=_NODEFAULT) -> typing.Any:
        def inner(node_or_func, /) -> typing.Any:
            namespace = {"node": "scalar", "__module__": node_or_func.__module__}

            if isinstance(node_or_func, type):
                bases: list[type[typing.Any]] = [node_or_func]
                node_bases = resolve_bases(node_or_func.__bases__)

                if not any(issubclass(base, Node) for base in node_bases if isinstance(base, type)):
                    bases.append(Node)
                    namespace["scope"] = NodeScope.PER_EVENT if scope is _NODEFAULT else scope
                elif scope is not _NODEFAULT:
                    namespace["scope"] = scope

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
    def compose(cls) -> type[Node]: ...


class GlobalNode[Value](Node):
    scope = NodeScope.GLOBAL

    @classmethod
    def set(cls, value: Value, /) -> None:
        NODE_CONTEXT.global_session[cls] = NodeSession(cls, value)

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

        if default is not sentinel and cls not in NODE_CONTEXT.global_sessions:
            return default

        if (session := NODE_CONTEXT.global_sessions.get(cls)) is None and default is sentinel:
            raise ValueError(f"Node `{fullname(cls)}` has no global value.")

        return session.value if session is not None else default

    @classmethod
    def unset(cls) -> None:
        NODE_CONTEXT.global_sessions.pop(cls, None)


__all__ = (
    "Composable",
    "ComposeError",
    "DataNode",
    "FactoryNode",
    "GlobalNode",
    "IsNode",
    "Name",
    "Node",
    "NodeClass",
    "NodeConvertable",
    "NodeProto",
    "NodeType",
    "as_node",
    "get_nodes",
    "is_node",
    "is_node_type",
    "scalar_node",
    "unwrap_node",
)
