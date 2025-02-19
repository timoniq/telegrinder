import typing

from telegrinder.node.base import IsNode, Node


class ContainerNode(Node):
    linked_nodes: typing.ClassVar[list[IsNode]]
    composer: typing.Callable[..., typing.Awaitable[typing.Any]]

    @classmethod
    async def compose(cls, **kw: typing.Any) -> typing.Any:
        subnodes = cls.get_subnodes().keys()
        return await cls.composer(*tuple(t[1] for t in sorted(kw.items(), key=lambda t: t[0]) if t[0] in subnodes))

    @classmethod
    def get_subnodes(cls) -> dict[str, IsNode]:
        subnodes = getattr(cls, "subnodes", None)
        if subnodes is None:
            subnodes_dct = {f"node_{i}": node_t for i, node_t in enumerate(cls.linked_nodes)}
            setattr(cls, "subnodes", subnodes_dct)
            return subnodes_dct
        return subnodes

    @classmethod
    def link_nodes(
        cls,
        linked_nodes: list[IsNode],
        composer: typing.Callable[..., typing.Awaitable[typing.Any]],
    ) -> type["ContainerNode"]:
        return type(cls.__name__, (cls,), {"linked_nodes": linked_nodes, "composer": classmethod(composer)})


__all__ = ("ContainerNode",)
