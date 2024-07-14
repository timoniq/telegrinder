import enum
import typing

if typing.TYPE_CHECKING:
    from .base import Node

T = typing.TypeVar("T", bound=type["Node"])


class NodeScope(enum.Enum):
    PER_EVENT = enum.auto()
    PER_CALL = enum.auto()


PER_EVENT = NodeScope.PER_EVENT
PER_CALL = NodeScope.PER_CALL


def per_call(node: T) -> T:
    setattr(node, "scope", PER_CALL)
    return node


def per_event(node: T) -> T:
    setattr(node, "scope", PER_EVENT)
    return node


__all__ = ("NodeScope", "PER_EVENT", "PER_CALL", "per_call", "per_event")
