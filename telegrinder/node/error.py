import dataclasses

import typing_extensions as typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, DataNode
from telegrinder.node.utility import TypeArgs

type ExceptionType = type[BaseException]

ExceptionT = typing.TypeVar("ExceptionT", bound=BaseException, default=BaseException)
ExceptionTs = typing.TypeVarTuple("ExceptionTs", default=typing.Unpack[tuple[BaseException, ...]])


def can_catch[ExceptionT: BaseException](
    exc: BaseException | ExceptionType,
    exc_types: type[ExceptionT] | tuple[type[ExceptionT], ...],
) -> typing.TypeGuard[ExceptionT]:
    return issubclass(exc, exc_types) if isinstance(exc, type) else isinstance(exc, exc_types)


@dataclasses.dataclass(kw_only=True, frozen=True)
class Error(DataNode, typing.Generic[*ExceptionTs]):
    __module__ = __name__

    exception_update: BaseException

    @property
    def exception(self: "Error[*tuple[ExceptionT, ...]]") -> ExceptionT:
        return self.exception_update  # type: ignore

    @classmethod
    def compose(cls, ctx: Context, type_args: TypeArgs) -> typing.Self:
        exception = ctx.exception_update.expect(ComposeError("No exception."))
        exception_types: tuple[ExceptionType, ...] | None = type_args.get(ExceptionTs)

        if exception_types is None or can_catch(exception, exception_types):
            return cls(exception_update=exception)

        raise ComposeError("Foreign exception.")


__all__ = ("Error",)
