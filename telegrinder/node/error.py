from __future__ import annotations

import dataclasses
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, DataNode
from telegrinder.node.utility import TypeArgs

type ExceptionType = type[Exception]


def can_catch[ExceptionT: Exception](
    exc: Exception | ExceptionType,
    exc_types: type[ExceptionT] | tuple[type[ExceptionT], ...],
) -> typing.TypeGuard[ExceptionT]:
    return issubclass(exc, exc_types) if isinstance(exc, type) else isinstance(exc, exc_types)


@dataclasses.dataclass(kw_only=True, frozen=True)
class Error[*Exceptions = *tuple[Exception, ...]](DataNode):
    exception_update: Exception

    @property
    def exception[T: Exception = Exception](self: Error[*tuple[T, ...]]) -> T:
        return self.exception_update  # type: ignore[UnknownReturnType]

    @classmethod
    def compose(cls, ctx: Context, type_args: TypeArgs) -> typing.Self:
        exception = ctx.exception_update.expect(ComposeError("No exception."))
        exception_types: tuple[ExceptionType, ...] | None = type_args.get(Exceptions)

        if exception_types is None or can_catch(exception, exception_types):
            return cls(exception_update=exception)

        raise ComposeError("Foreign exception.")


__all__ = ("Error",)
