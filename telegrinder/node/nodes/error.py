from __future__ import annotations

import dataclasses
import typing

from nodnod.error import NodeError
from nodnod.interface.data import DataNode
from nodnod.interface.generic import generic_node

from telegrinder.bot.dispatch.context import Context

type ExceptionType = type[Exception]


def can_catch[ExceptionT: Exception](
    exc: Exception | ExceptionType,
    exc_types: type[ExceptionT] | tuple[type[ExceptionT], ...],
) -> typing.TypeGuard[ExceptionT]:
    return issubclass(exc, exc_types) if isinstance(exc, type) else isinstance(exc, exc_types)


@generic_node
@dataclasses.dataclass(kw_only=True, frozen=True)
class Error[*Exceptions = *tuple[type[Exception], ...]](DataNode):
    exception_update: Exception

    @property
    def exception[T: Exception = Exception](self: Error[*tuple[T, ...]]) -> T:
        return self.exception_update  # type: ignore[reportReturnType]

    @classmethod
    def __compose__(
        cls,
        exceptions: tuple[typing.Unpack[Exceptions]],
        context: Context,
    ) -> typing.Self:
        exception_update = context.exception_update.expect(NodeError("No exception."))

        if can_catch(exception_update, exceptions):  # type: ignore
            return cls(exception_update=exception_update)

        raise NodeError("Foreign exception.")


__all__ = ("Error",)
