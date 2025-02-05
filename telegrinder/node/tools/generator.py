import inspect
import typing

from telegrinder.node.base import ComposeError, Node
from telegrinder.node.container import ContainerNode


def cast_false_to_none[Value](value: Value) -> Value | None:
    if value is False:
        return None
    return value


def error_on_none[Value](value: Value | None) -> Value:
    if value is None:
        raise ComposeError
    return value


def generate_node(
    subnodes: tuple[type[Node], ...],
    func: typing.Callable[..., typing.Any],
    casts: tuple[typing.Callable[[typing.Any], typing.Any], ...] = (cast_false_to_none, error_on_none),
) -> type[Node]:
    async def compose(cls, *args: typing.Any) -> typing.Any:
        result = func(*args)
        if inspect.isawaitable(result):
            result = await result
        for cast in casts:
            result = cast(result)
        return result

    return ContainerNode.link_nodes(linked_nodes=list(subnodes), composer=compose)


__all__ = ("generate_node",)
