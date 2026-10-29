from contextlib import suppress

import kungfu
import typing_extensions as typing
from msgspex.model import Model
from nodnod.interface.composable import Composable
from nodnod.utils.is_type import is_type

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node import EventNode
from telegrinder.tools.member_descriptor_proxy import MemberDescriptorProxy, evaluate_operations

type NodeLike[T = typing.Any] = typing.TypeForm[T]
type AnyModel[T: Model] = typing.TypeForm[T]

_MISSING: typing.Final = object()


class Magic[R, **P = [R]](kungfu.F[R, P], ABCRule):
    node: NodeLike | None

    @typing.overload
    def __init__[T](self: Magic[T], *, node: NodeLike[T]) -> None: ...

    @typing.overload
    def __init__[T: Model](self: Magic[T], model: AnyModel[T], /) -> None: ...

    @typing.overload
    def __init__[T: Model](self: Magic[T], model: AnyModel[T], /, parent: NodeLike | None = None) -> None: ...

    @typing.overload
    def __init__(cls, field: R, /, parent: NodeLike | None = None) -> None: ...

    def __init__(
        self,
        obj: typing.Any = _MISSING,
        parent: NodeLike | None = None,
        *,
        node: typing.Any = _MISSING,
    ) -> None:
        if obj is _MISSING and not is_type(node, Composable):
            raise ValueError("First positional argument is required or `node` must be provided as a composable object.")

        obj = node if obj is _MISSING else obj

        if isinstance(obj, MemberDescriptorProxy):
            owner_cls, member_name, operations = obj._objclass, obj._member_name, obj._operations
            node = (
                owner_cls if is_type(owner_cls, Composable) else typing.cast("NodeLike", EventNode[owner_cls])  # type: ignore
            )
            super().__init__(lambda obj: evaluate_operations(obj, member_name, operations))  # type: ignore

        elif is_type(obj, Composable):
            node = obj
            super().__init__()  # type: ignore

        else:
            node = parent
            super().__init__(obj)

        self.node = node
        self.required_nodes = dict(magic_value=node)

    def check(self, magic_value: typing.Any) -> bool:
        with suppress(kungfu.UnwrapError):
            self(magic_value)  # type: ignore
            return True

        return False

    def new(self, f: typing.Any, /) -> typing.Any:
        return Magic(f, parent=self.node)

    if typing.TYPE_CHECKING:

        def then[T](self, g: typing.Callable[[R], T], /) -> "Magic[T, P]": ...

        def ensure(
            self,
            chk: typing.Callable[[R], bool],
            error: typing.Callable[[R], BaseException] | BaseException | str | None = None,
        ) -> "Magic[R, P]": ...

        def expect[T, Err](
            self: kungfu.F[kungfu.Result[T, Err], P],
            error: typing.Callable[[kungfu.Result[T, Err]], BaseException] | BaseException | str | None = None,
        ) -> "Magic[T, P]": ...


__all__ = ("Magic",)
