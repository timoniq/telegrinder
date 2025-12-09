import typing

from nodnod.error import NodeError
from nodnod.node import Node
from nodnod.value import Value

from telegrinder.node.scope import TELEGRINDER_CONTEXT, global_node
from telegrinder.tools.fullname import fullname

NODEFAULT: typing.Final = object()

_Unspecialized = typing.NewType("_Unspecialized", type)


@global_node
class GlobalNode[T = _Unspecialized](Node):
    @typing.overload
    @classmethod
    def set(cls: type[GlobalNode[_Unspecialized]], value: typing.Self, /) -> None: ...  # type: ignore

    @typing.overload
    @classmethod
    def set(cls, value: T, /) -> None: ...

    @classmethod
    def set(cls, value: T | typing.Self, /) -> None:
        TELEGRINDER_CONTEXT.node_global_scope.push(Value(cls, value))

    @typing.overload
    @classmethod
    def get(cls: type[GlobalNode[_Unspecialized]], /) -> typing.Self:  # type: ignore
        ...

    @typing.overload
    @classmethod
    def get(cls) -> T: ...

    @typing.overload
    @classmethod
    def get[Default](cls: type[GlobalNode[_Unspecialized]], *, default: Default) -> typing.Self | Default:  # type: ignore
        ...

    @typing.overload
    @classmethod
    def get[Default](cls, *, default: Default) -> T | Default: ...

    @classmethod
    def get(cls, *, default: typing.Any = NODEFAULT) -> typing.Any:
        if default is not NODEFAULT and cls not in TELEGRINDER_CONTEXT.node_global_scope:
            return default

        if (value := TELEGRINDER_CONTEXT.node_global_scope.get(cls)) is None and default is NODEFAULT:
            raise NodeError(f"Node `{fullname(cls)}` has no global value.")

        return value.value if value is not None else default

    @classmethod
    def unset(cls) -> None:
        TELEGRINDER_CONTEXT.node_global_scope.pop(cls, None)

    @classmethod
    def __compose__(cls) -> T:
        return cls.get()


__all__ = ("GlobalNode",)
