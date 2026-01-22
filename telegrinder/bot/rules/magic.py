import typing
from contextlib import suppress

import kungfu

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node import EventNode
from telegrinder.node.utils import is_node
from telegrinder.tools.member_descriptor_proxy import MemberDescriptorProxy, evaluate_operations


class Magic[R, **P = [R]](kungfu.F[R, P], ABCRule):
    def __init__(
        self,
        field: R,
        parent: typing.Any = None,
    ) -> None:
        if isinstance(field, MemberDescriptorProxy):
            owner_cls, member_name, operations = field._objclass, field._member_name, field._operations
            node = EventNode[owner_cls]
            super().__init__(lambda obj: evaluate_operations(obj, member_name, operations))  # type: ignore

        elif is_node(field):
            node = field
            super().__init__()  # type: ignore

        else:
            node = parent
            super().__init__(field)  # type: ignore

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
