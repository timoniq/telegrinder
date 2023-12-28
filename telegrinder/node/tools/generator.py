import typing

from telegrinder.node.base import Node
from telegrinder.node.container import ContainerNode

T = typing.TypeVar("T")


def cast_false_to_none(value: T) -> T | None:
    if value is False:
        return None
    return value


def generate(
    subnodes: tuple[type[Node], ...], 
    func: typing.Callable[..., typing.Any],
    casts: tuple[typing.Callable, ...] = (cast_false_to_none,),
) -> type[ContainerNode]:
    async def compose(cls, **kw) -> typing.Any:
        args = await super(cls).compose(**kw)
        return func(args)

    return ContainerNode.link_nodes(list(subnodes))
