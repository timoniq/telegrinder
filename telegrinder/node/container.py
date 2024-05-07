import typing

from .base import Node


class ContainerNode(Node):
    linked_nodes: typing.ClassVar[list[type[Node]]]

    @classmethod
    async def compose(cls, **kw) -> tuple["Node", ...]:
        return tuple(t[1] for t in sorted(kw.items(), key=lambda t: t[0]))

    @classmethod
    def get_sub_nodes(cls) -> dict[str, type["Node"]]:
        return {f"node_{i}": node_t for i, node_t in enumerate(cls.linked_nodes)}

    @classmethod
    def link_nodes(cls, linked_nodes: list[type[Node]]) -> type["ContainerNode"]:
        return type("_ContainerNode", (cls,), {"linked_nodes": linked_nodes})


__all__ = ("ContainerNode",)
