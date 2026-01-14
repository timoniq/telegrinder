import sys
import typing

from nodnod.node import Node

from telegrinder.tools.fullname import fullname


def is_node(maybe_node: typing.Any, /) -> bool:
    return isinstance(maybe_node, type) and issubclass(maybe_node, Node)


def as_node(obj: typing.Any, /) -> type[Node[typing.Any, typing.Any]]:
    if not is_node(obj):
        raise TypeError(f"Object `{fullname(obj)}` is not a node.")
    return obj


def get_locals_from_function(func: typing.Callable[..., typing.Any], /) -> typing.Mapping[str, typing.Any] | None:
    bound_class = func.__self__ if hasattr(func, "__self__") else None
    bound_class = func.__objclass__ if bound_class is None and hasattr(func, "__objclass__") else None

    if bound_class is not None:
        return (bound_class if isinstance(bound_class, type) else type(bound_class)).__dict__

    return None


def get_globals_from_function(func: typing.Callable[..., typing.Any], /) -> dict[str, typing.Any]:
    if hasattr(func, "__globals__"):
        return getattr(func, "__globals__")

    module = getattr(func, "__module__", type(func).__module__)

    if module in sys.modules:
        return vars(sys.modules[module])

    return {}


__all__ = ("as_node", "get_globals_from_function", "get_locals_from_function", "is_node")
