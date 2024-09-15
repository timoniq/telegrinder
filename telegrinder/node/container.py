import typing

from telegrinder.node.base import Node


class ContainerNode(Node):
    linked_nodes: typing.ClassVar[list[type[Node]]]

    @classmethod
    def compose(cls, **kw) -> tuple[Node, ...]:
        return tuple(t[1] for t in sorted(kw.items(), key=lambda t: t[0]))

    @classmethod
    def get_subnodes(cls) -> dict[str, type[Node]]:
        subnodes = getattr(cls, "subnodes", None)
        if subnodes is None:
            subnodes_dct = {f"node_{i}": node_t for i, node_t in enumerate(cls.linked_nodes)}
            setattr(cls, "subnodes", subnodes_dct)
            return subnodes_dct
        return subnodes

    @classmethod
    def link_nodes(cls, linked_nodes: list[type[Node]]) -> type["ContainerNode"]:
        return type("_ContainerNode", (cls,), {"linked_nodes": linked_nodes})


__all__ = ("ContainerNode",)
