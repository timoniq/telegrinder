import inspect
import types
import typing

import fntypes

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node import EventNode, is_node


class Magic[R, **P = [R]](fntypes.F[R, P], ABCRule):
    def __init__(
        self,
        field: R,
        parent: typing.Any = None,
    ):
        is_member = isinstance(field, types.MemberDescriptorType) or inspect.ismemberdescriptor(field)

        if is_member:
            owner_cls = getattr(field, "__objclass__")
            attr_name = getattr(field, "__name__")

            self.node = EventNode[owner_cls]
            super().__init__(lambda x: getattr(x, attr_name))  # type: ignore

        elif is_node(field):
            self.node = field
            super().__init__()  # type: ignore

        else:
            self.node = parent
            super().__init__(field)  # type: ignore

    async def check(self, node) -> bool:
        try:
            self(node)  # type: ignore
        except fntypes.UnwrapError:
            return False
        return True

    def new(self, f):
        return Magic(f, parent=self.node)

    @property
    def required_nodes(self):
        return {"node": self.node}

    if typing.TYPE_CHECKING:

        def then[T](self, g: typing.Callable[[R], T], /) -> "Magic[T, P]": ...

        def ensure(
            self,
            chk: typing.Callable[[R], bool],
            error: typing.Callable[[R], BaseException] | BaseException | str | None = None,
        ) -> "Magic[R, P]": ...

        def expect[T, Err](
            self: fntypes.F[fntypes.Result[T, Err], P],
            error: typing.Callable[[fntypes.Result[T, Err]], BaseException] | BaseException | str | None = None,
        ) -> "Magic[T, P]": ...
