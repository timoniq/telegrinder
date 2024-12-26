import abc
import inspect
from types import AsyncGeneratorType

import typing_extensions as typing

from telegrinder.node.scope import NodeScope
from telegrinder.tools.magic import cache_magic_value, get_annotations

T = typing.TypeVar("T", default=typing.Any)

ComposeResult: typing.TypeAlias = T | typing.Awaitable[T] | typing.AsyncGenerator[T, None]


def is_node(maybe_node: typing.Any) -> typing.TypeGuard[type["Node"]]:
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
    Provides caching for passed node type."""

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


class ScalarNodeProto(Node, abc.ABC):
    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass


SCALAR_NODE = type("ScalarNode", (), {"node": "scalar"})


if typing.TYPE_CHECKING:

    class ScalarNode(ScalarNodeProto, abc.ABC):
        pass

else:

    def __init_subclass__(cls, *args, **kwargs):  # noqa: N807
        if any(issubclass(base, ScalarNodeProto) for base in cls.__bases__ if base is not ScalarNode):
            raise RuntimeError("Scalar nodes do not support inheritance.")

    def _as_node(cls, bases, dct):
        if not hasattr(cls, "_scalar_node_type"):
            dct.update(cls.__dict__)
            scalar_node_type = type(cls.__name__, bases, dct)
            setattr(cls, "_scalar_node_type", scalar_node_type)
            return scalar_node_type
        return getattr(cls, "_scalar_node_type")

    def create_class(name, bases, dct):
        return type(
            "Scalar",
            (SCALAR_NODE,),
            {
                "as_node": classmethod(lambda cls: _as_node(cls, bases, dct)),
                "scope": Node.scope,
                "__init_subclass__": __init_subclass__,
            },
        )

    class ScalarNode(ScalarNodeProto, abc.ABC, metaclass=create_class):
        pass


class Name(ScalarNode, str):
    @classmethod
    def compose(cls) -> str: ...


class GlobalNode(Node):
    scope = NodeScope.GLOBAL

    @classmethod
    def set(cls, value: typing.Self, /) -> None:
        setattr(cls, "_value", value)

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
    "SCALAR_NODE",
    "ScalarNode",
    "ScalarNodeProto",
    "get_nodes",
    "is_node",
)
