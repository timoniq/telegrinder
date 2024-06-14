import inspect
import typing

from telegrinder.node.base import ComposeError, Node
from telegrinder.node.container import ContainerNode

T = typing.TypeVar("T")


def cast_false_to_none(value: T) -> T | None:
    if value is False:
        return None
    return value


def error_on_none(value: T | None) -> T:
    if value is None:
        raise ComposeError
    return value


def generate_node(
    subnodes: tuple[type[Node], ...],
    func: typing.Callable[..., typing.Any],
    casts: tuple[typing.Callable[[typing.Any], typing.Any], ...] = (cast_false_to_none, error_on_none),
) -> type[ContainerNode]:
    async def compose(**kw: typing.Any) -> typing.Any:
        args = await ContainerNode.compose(**kw)
        result = func(*args)
        if inspect.isawaitable(result):
            result = await result
        for cast in casts:
            result = cast(result)
        return result

    container = ContainerNode.link_nodes(list(subnodes))
    return type("_ContainerNode", (container,), {"compose": compose})


__all__ = ("generate_node",)
