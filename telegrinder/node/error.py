import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.base import ComposeError, Node
from telegrinder.node.either import Optional
from telegrinder.node.utility import TypeArgs


def can_catch(exc: Exception, exception_t: type[Exception] | tuple[type[Exception]]):
    if isinstance(exc, type):
        return issubclass(exc.__class__, exception_t)
    return isinstance(exc, exception_t)


# TODO: *ExceptionTs
# err: Error[RuntimeError, AnotherError]
# passes on both errors; err.exception ~ Union[*ExceptionTs]
class Error[ExceptionT: Exception](Node):
    def __init__(self, exception: ExceptionT):
        self.exception = exception

    @classmethod
    def compose(cls, ctx: Context, args: TypeArgs) -> typing.Self:
        if "_exception" not in ctx:
            raise ComposeError("No exception")

        exception = ctx["_exception"]
        exception_t = typing.cast("type[Exception]", args["ExceptionT"])

        if exception_t is None:
            # Any exception (err: Error)
            return cls(exception=exception)

        if not can_catch(exception, exception_t):
            raise ComposeError("Foreign exception type")

        return cls(exception=exception)
