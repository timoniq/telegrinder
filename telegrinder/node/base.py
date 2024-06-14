import abc
import inspect
import typing

ComposeResult: typing.TypeAlias = typing.Coroutine[typing.Any, typing.Any, typing.Any] | typing.AsyncGenerator[typing.Any, None]


class ComposeError(BaseException): ...


class Node(abc.ABC):
    node: str = "node"

    @classmethod
    @abc.abstractmethod
    def compose(cls, *args, **kwargs) -> ComposeResult:
        pass

    @classmethod
    def compose_error(cls, error: str | None = None) -> typing.NoReturn:
        raise ComposeError(error)

    @classmethod
    def get_sub_nodes(cls) -> dict[str, type[typing.Self]]:
        parameters = inspect.signature(cls.compose).parameters

        sub_nodes = {}
        for name, param in parameters.items():
            if param.annotation is inspect._empty:
                continue
            node = param.annotation
            sub_nodes[name] = node
        return sub_nodes

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
            {"as_node": classmethod(lambda cls: create_node(cls, bases, dct))},
        )

    class ScalarNode(ScalarNodeProto, abc.ABC, metaclass=create_class):
        pass


__all__ = (
    "ComposeError",
    "DataNode",
    "Node",
    "SCALAR_NODE",
    "ScalarNode",
)
