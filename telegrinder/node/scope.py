from __future__ import annotations

import enum
import typing

if typing.TYPE_CHECKING:
    from telegrinder.node.base import Composable

NODE_SCOPE_KEY: typing.Final[str] = "scope"


class NodeScope(enum.Enum):
    GLOBAL = enum.auto()
    PER_EVENT = enum.auto()
    PER_CALL = enum.auto()


PER_EVENT = NodeScope.PER_EVENT
PER_CALL = NodeScope.PER_CALL
GLOBAL = NodeScope.GLOBAL


def per_call[T: Composable[typing.Any]](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_CALL)
    return node


def per_event[T: Composable[typing.Any]](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_EVENT)
    return node


def global_node[T: Composable[typing.Any]](node: type[T]) -> type[T]:
    setattr(node, "scope", GLOBAL)
    return node


def get_scope(node: Composable[typing.Any], /) -> NodeScope | None:
    return getattr(node, NODE_SCOPE_KEY, None)


__all__ = (
    "GLOBAL",
    "NodeScope",
    "PER_CALL",
    "PER_EVENT",
    "get_scope",
    "global_node",
    "per_call",
    "per_event",
)
