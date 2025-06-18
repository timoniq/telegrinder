import dataclasses
import typing

from telegrinder.node.base import IsNode, Node, as_node
from telegrinder.tools.magic.annotations import Annotations


class Collection(Node):
    __subnodes__: typing.ClassVar[dict[str, IsNode] | None] = None

    @classmethod
    def get_subnodes(cls) -> dict[str, IsNode]:
        if cls.__subnodes__ is None:
            cls.__subnodes__ = {
                name: node
                for name, annotation in Annotations(obj=cls).get(cache=True, exclude_forward_refs=True).items()
                if (node := as_node(annotation, raise_exception=False)) is not None
            }

        return cls.__subnodes__

    @classmethod
    def compose(cls, **kwargs: typing.Any) -> typing.Self:
        subnodes = cls.__subnodes__ or {}

        if dataclasses.is_dataclass(cls):
            return cls(**{name: kwargs[name] for name in subnodes if name in kwargs})

        instance = cls()
        for name in subnodes:
            if name in kwargs:
                setattr(instance, name, kwargs[name])

        return instance


__all__ = ("Collection",)
