import typing

from telegrinder.node.base import IsNode, Node
from telegrinder.node.container import ContainerNode
from telegrinder.node.exceptions import ComposeError
from telegrinder.tools.aio import maybe_awaitable


def cast_false_to_none[Value](value: Value) -> Value | None:
    if value is False:
        return None
    return value


def error_on_none[Value](value: Value | None) -> Value:
    if value is None:
        raise ComposeError
    return value


def generate_node(
    subnodes: tuple[IsNode, ...],
    func: typing.Callable[..., typing.Any],
    casts: tuple[typing.Callable[[typing.Any], typing.Any], ...] = (cast_false_to_none, error_on_none),
) -> type[Node]:
    async def compose(_, *args: typing.Any) -> typing.Any:
        result = await maybe_awaitable(func(*args))
        for cast in casts:
            result = cast(result)
        return result

    return ContainerNode.link_nodes(linked_nodes=list(subnodes), composer=compose)


__all__ = ("generate_node",)
