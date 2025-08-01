from __future__ import annotations

import enum
import typing

NODE_SCOPE_KEY: typing.Final[str] = "scope"


class NodeScope(enum.Enum):
    GLOBAL = enum.auto()
    PER_EVENT = enum.auto()
    PER_CALL = enum.auto()


PER_EVENT = NodeScope.PER_EVENT
PER_CALL = NodeScope.PER_CALL
GLOBAL = NodeScope.GLOBAL


def per_call[T](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_CALL)
    return node


def per_event[T](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_EVENT)
    return node


def global_node[T](node: type[T]) -> type[T]:
    setattr(node, "scope", GLOBAL)
    return node


def get_scope(node: typing.Any, /) -> NodeScope:
    return getattr(node, NODE_SCOPE_KEY, PER_EVENT)


__all__ = (
    "GLOBAL",
    "PER_CALL",
    "PER_EVENT",
    "NodeScope",
    "get_scope",
    "global_node",
    "per_call",
    "per_event",
)
