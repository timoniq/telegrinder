import abc
import inspect
from types import AsyncGeneratorType, resolve_bases

import typing_extensions as typing

from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import cache_magic_value, get_annotations

T = typing.TypeVar("T", default=typing.Any)
X = typing.TypeVar("X", default=typing.Never)

ComposeResult: typing.TypeAlias = T | typing.Awaitable[T] | typing.AsyncGenerator[T, None]


@typing.overload
def is_node(maybe_node: type[typing.Any], /) -> typing.TypeGuard[type["Node"]]: ...


@typing.overload
def is_node(maybe_node: typing.Any, /) -> typing.TypeGuard["Node"]: ...


def is_node(maybe_node: typing.Any, /) -> typing.TypeGuard["Node | type[Node]"]:
    if isinstance(maybe_node, typing.TypeAliasType):
        maybe_node = maybe_node.__value__
    if not isinstance(maybe_node, type):
        maybe_node = typing.get_origin(maybe_node) or maybe_node

    return (
        isinstance(maybe_node, type)
        and issubclass(maybe_node, Node)
        or isinstance(maybe_node, Node)
        or hasattr(maybe_node, "as_node")
    )


@cache_magic_value("__nodes__")
def get_nodes(function: typing.Callable[..., typing.Any]) -> dict[str, type["Node"]]:
    return {k: v for k, v in get_annotations(function).items() if is_node(v)}


@cache_magic_value("__is_generator__")
def is_generator(
    function: typing.Callable[..., typing.Any],
) -> typing.TypeGuard[AsyncGeneratorType[typing.Any, None]]:
    return inspect.isasyncgenfunction(function)


def get_node_calc_lst(node: type["Node"]) -> list[type["Node"]]:
    """Returns flattened list of node types in ordering required to calculate given node.
    Provides caching for passed node type.
    """
    if calc_lst := getattr(node, "__nodes_calc_lst__", None):
        return calc_lst
    nodes_lst: list[type[Node]] = []
    for node_type in node.as_node().get_subnodes().values():
        nodes_lst.extend(get_node_calc_lst(node_type))
    calc_lst = [*nodes_lst, node]
    setattr(node, "__nodes_calc_lst__", calc_lst)
    return calc_lst


class ComposeError(BaseException):
    pass


class NodeProto[T](typing.Protocol):
    @classmethod
    def compose(cls, *args: typing.Any, **kwargs: typing.Any) -> ComposeResult[T]: ...


class Node(abc.ABC):
    node: str = "node"
    scope: NodeScope = NodeScope.PER_EVENT

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @classmethod
    def compose_error(cls, error: str | None = None) -> typing.NoReturn:
        raise ComposeError(error)

    @classmethod
    def get_subnodes(cls) -> dict[str, type["Node"]]:
        return get_nodes(cls.compose)

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> bool:
        return is_generator(cls.compose)


@typing.overload
def scalar_node[T]() -> typing.Callable[[type[NodeProto[T]]], type[T]]: ...


@typing.overload
def scalar_node[T](*types: type[T]) -> typing.Callable[[type[NodeProto[typing.Any]]], type[T]]: ...


def scalar_node(*types):
    def wrapper[R](node, /):
        bases: list[type[typing.Any]] = [node]
        node_bases = resolve_bases(node.__bases__)
        if not any(issubclass(base, Node) for base in node_bases if isinstance(base, type)):
            bases.append(Node)
        return type("Scalar" + node.__name__, tuple(bases), {})  # type: ignore

    return wrapper


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


@scalar_node()
class Name:
    @classmethod
    def compose(cls) -> str: ...


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
    "ComposeError",
    "DataNode",
    "FactoryNode",
    "GlobalNode",
    "Name",
    "Node",
    "scalar_node",
    "get_nodes",
    "is_node",
)
