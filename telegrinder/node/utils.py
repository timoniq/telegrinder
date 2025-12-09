import typing

from nodnod.node import Node

from telegrinder.tools.fullname import fullname


def is_node(maybe_node: typing.Any, /) -> bool:
    return isinstance(maybe_node, type) and issubclass(maybe_node, Node)


def as_node(obj: typing.Any, /) -> type[Node[typing.Any, typing.Any]]:
    if not is_node(obj):
        raise TypeError(f"Object `{fullname(obj)}` is not a node.")
    return obj


__all__ = ("as_node", "is_node")
