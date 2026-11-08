import sys
import types
import typing
from inspect import unwrap

from nodnod.interface.is_node import is_node
from nodnod.node import Node
from nodnod.utils.create_node import create_node

from telegrinder.tools.fullname import fullname

UNSET_NODE_ATTRS: typing.Final = types.MappingProxyType[str, None](
    mapping=dict[str, None].fromkeys(
        {
            "__type__",
            "__dependencies__",
            "__injections__",
            "__map__",
            "__initialize__",
            "__compose_names_by_type__",
        },
    ),
)


def as_node(obj: typing.Any, /) -> type[Node[typing.Any, typing.Any]]:
    if not is_node(obj):
        raise TypeError(f"Object `{fullname(obj)}` is not a node.")
    return obj


def get_locals_from_function(func: typing.Callable[..., typing.Any], /) -> typing.Mapping[str, typing.Any] | None:
    f = unwrap(func)
    bound_class = f.__self__ if hasattr(f, "__self__") else None
    bound_class = f.__objclass__ if bound_class is None and hasattr(f, "__objclass__") else None

    if bound_class is not None:
        return (bound_class if isinstance(bound_class, type) else type(bound_class)).__dict__

    return None


def get_globals_from_function(func: typing.Callable[..., typing.Any], /) -> dict[str, typing.Any]:
    f = unwrap(func)

    if hasattr(f, "__globals__"):
        return getattr(f, "__globals__")

    module = getattr(f, "__module__", type(f).__module__)

    if module in sys.modules:
        return vars(sys.modules[module])

    return {}


def create_node_from_scratch(
    name: str,
    bases: tuple[type[typing.Any], ...],
    namespace: dict[str, typing.Any] | None = None,
    /,
    **kwds: typing.Any,
) -> type[Node]:
    return create_node(
        name,
        Node,
        bases,
        UNSET_NODE_ATTRS | (namespace or {}),
        **kwds,
    )


__all__ = ("as_node", "create_node_from_scratch", "get_globals_from_function", "get_locals_from_function", "is_node")
