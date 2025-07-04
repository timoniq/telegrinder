import dataclasses
import typing

import msgspec

from telegrinder.node.base import IsNode, Node, as_node
from telegrinder.tools.magic.annotations import Annotations
from telegrinder.tools.magic.dictionary import extract


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
        nodes = extract(cls.__subnodes__ or (), kwargs)

        if dataclasses.is_dataclass(cls) or issubclass(cls, msgspec.Struct):
            return cls(**nodes)

        instance = cls()
        for name, value in nodes.items():
            setattr(instance, name, value)

        return instance


__all__ = ("Collection",)
