import enum
import typing

if typing.TYPE_CHECKING:
    from .base import IsNode


class NodeScope(enum.Enum):
    GLOBAL = enum.auto()
    PER_EVENT = enum.auto()
    PER_CALL = enum.auto()


PER_EVENT = NodeScope.PER_EVENT
PER_CALL = NodeScope.PER_CALL
GLOBAL = NodeScope.GLOBAL


def per_call[T: IsNode](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_CALL)
    return node


def per_event[T: IsNode](node: type[T]) -> type[T]:
    setattr(node, "scope", PER_EVENT)
    return node


def global_node[T: IsNode](node: type[T]) -> type[T]:
    setattr(node, "scope", GLOBAL)
    return node


__all__ = (
    "GLOBAL",
    "NodeScope",
    "PER_CALL",
    "PER_EVENT",
    "global_node",
    "per_call",
    "per_event",
)
