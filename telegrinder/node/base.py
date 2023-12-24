import abc
import inspect
import types
import typing
from dataclasses import dataclass

from telegrinder.types import Update


class ComposeError(Exception):
    pass


T = typing.TypeVar("T")


class Node(abc.ABC):
    node: str = "node"

    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> "typing.Self":
        pass

    @classmethod
    def compose_error(cls, error: str | None = None) -> typing.NoReturn:
        raise ComposeError(error)
    
    @classmethod
    def get_sub_nodes(cls) -> dict[str, type["Node"]]:
        parameters = inspect.signature(cls.compose).parameters
        
        sub_nodes = {}
        for name, param in parameters.items():
            node = param.annotation
            sub_nodes[name] = node
        return sub_nodes
    
    @classmethod
    def as_node(cls) -> type["typing.Self"]:
        return cls


class DataNode(Node, abc.ABC):
    node = "data"

    @typing.dataclass_transform()
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> "typing.Self":
        pass


class ScalarNodeProto(Node, abc.ABC):
    
    @classmethod
    @abc.abstractmethod
    async def compose(cls, *args, **kwargs) -> "typing.Self":
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
