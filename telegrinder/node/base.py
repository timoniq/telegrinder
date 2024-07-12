import abc
import inspect
import typing

from telegrinder.tools.magic import get_annotations

from .scope import NodeScope

ComposeResult: typing.TypeAlias = (
    typing.Coroutine[typing.Any, typing.Any, typing.Any]
    | typing.AsyncGenerator[typing.Any, None]
    | typing.Any
)


class ComposeError(BaseException): ...


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
    def get_sub_nodes(cls) -> dict[str, type[typing.Self]]:
        return get_annotations(cls.compose)

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def is_generator(cls) -> bool:
        return inspect.isasyncgenfunction(cls.compose)


class DataNode(Node, abc.ABC):
    node = "data"

    @typing.dataclass_transform()
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> ComposeResult:
        pass


class ScalarNodeProto(Node, abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> ComposeResult:
        pass


SCALAR_NODE = type("ScalarNode", (), {"node": "scalar"})


if typing.TYPE_CHECKING:

    class ScalarNode(ScalarNodeProto, abc.ABC):
        pass

else:

    def create_node(cls, bases, dct):
        dct.update(cls.__dict__)
        return type(cls.__name__, bases, dct)

    def create_class(name, bases, dct):
        return type(
            "Scalar",
            (SCALAR_NODE,),
            {
                "as_node": classmethod(lambda cls: create_node(cls, bases, dct)),
                "scope": Node.scope,
            },
        )

    class ScalarNode(ScalarNodeProto, abc.ABC, metaclass=create_class):
        pass


def is_node(maybe_node: type[typing.Any]) -> typing.TypeGuard[type[Node]]:
    maybe_node = typing.get_origin(maybe_node) or maybe_node
    return (
        isinstance(maybe_node, type)
        and issubclass(maybe_node, Node)
        or isinstance(maybe_node, Node)
        or hasattr(maybe_node, "as_node")
    )


__all__ = (
    "ComposeError",
    "DataNode",
    "Node",
    "SCALAR_NODE",
    "ScalarNode",
    "is_node",
)
