import dataclasses
from functools import cached_property

import typing_extensions as typing
from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

Function = typing.TypeVar("Function", bound="Func[..., typing.Any]")
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)

type Func[**P, Result] = typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, Result]]


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler(ABCHandler, typing.Generic[Function, ErrorHandlerT]):
    function: Function
    rules: list["ABCRule"]
    final: bool = dataclasses.field(default=True, kw_only=True)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast("ErrorHandlerT", ErrorHandler()),
        kw_only=True,
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)

    @property
    def __call__(self) -> Function:
        return self.function

    def __str__(self) -> str:
        return fullname(self.function)

    def __repr__(self) -> str:
        return "<{} {!r} with rules={!r}, error_handler={!r}>".format(
            ("final " if self.final else "") + type(self).__name__,
            fullname(self.function),
            self.rules,
            self.error_handler,
        )

    @cached_property
    def required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.function)

    async def run(
        self,
        api: API,
        event: Update,
        context: Context,
    ) -> Result[typing.Any, str]:
        logger.debug(f"Checking rules and composing nodes for handler `{self}`...")

        temp_ctx = context.copy()
        temp_ctx |= self.preset_context.copy()
        for rule in self.rules:
            if not await check_rule(api, rule, event, temp_ctx):
                return Error(f"Rule {rule!r} failed!")

        context |= temp_ctx
        node_col = None

        if self.required_nodes:
            match await compose_nodes(self.required_nodes, context, data={Update: event, API: api}):
                case Ok(value):
                    node_col = value
                case Error(compose_error):
                    return Error(f"Cannot compose nodes for handler `{self}`, error: {compose_error.message}")

        logger.debug(f"All good, running handler `{self}`...")

        try:
            data_bundle = bundle(
                self.function, {API: api, Update: event, Context: context.copy()}, typebundle=True
            )
            return Ok(
                await bundle(self.function, context | ({} if node_col is None else node_col.values), start_idx=0)(
                    *data_bundle.args, **data_bundle.kwargs
                ),
            )
        except BaseException as exception:
            return Ok(await self.error_handler.run(exception, event, api, context))
        finally:
            if node_col is not None:
                await node_col.close_all()


__all__ = ("FuncHandler",)
