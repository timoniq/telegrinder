import enum
import typing

if typing.TYPE_CHECKING:
    from .base import Node

T = typing.TypeVar("T", bound=type["Node"])


class NodeScope(enum.Enum):
    GLOBAL = enum.auto()
    PER_EVENT = enum.auto()
    PER_CALL = enum.auto()


PER_EVENT = NodeScope.PER_EVENT
PER_CALL = NodeScope.PER_CALL
GLOBAL = NodeScope.GLOBAL


def per_call(node: T) -> T:
    setattr(node, "scope", PER_CALL)
    return node


def per_event(node: T) -> T:
    setattr(node, "scope", PER_EVENT)
    return node


def global_node(node: T) -> T:
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
