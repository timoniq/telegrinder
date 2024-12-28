import dataclasses
from functools import cached_property

import typing_extensions as typing

from telegrinder.api.api import API
from telegrinder.bot.adapter.abc import ABCAdapter
from telegrinder.bot.adapter.dataclass import DataclassAdapter
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.node.base import Node, get_nodes
from telegrinder.node.composer import NodeCollection, compose_nodes
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.tools.magic import get_annotations, magic_bundle
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.composer import NodeCollection

Function = typing.TypeVar("Function", bound="Func[..., typing.Any]")
Event = typing.TypeVar("Event")
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)

type Func[**Rest, Result] = typing.Callable[Rest, typing.Coroutine[typing.Any, typing.Any, Result]]


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler(ABCHandler[Event], typing.Generic[Event, Function, ErrorHandlerT]):
    function: Function
    rules: list["ABCRule"]
    adapter: ABCAdapter[Update, Event] | None = dataclasses.field(default=None, kw_only=True)
    is_blocking: bool = dataclasses.field(default=True, kw_only=True)
    dataclass: type[typing.Any] | None = dataclasses.field(default=dict[str, typing.Any], kw_only=True)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast(ErrorHandlerT, ErrorHandler()),
        kw_only=True,
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)
    update_type: UpdateType | None = dataclasses.field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        self.dataclass = typing.get_origin(self.dataclass) or self.dataclass

        if self.dataclass is not None and self.adapter is None:
            self.adapter = DataclassAdapter(self.dataclass, self.update_type)

    @property
    def __call__(self) -> Function:
        return self.function

    def __repr__(self) -> str:
        return "<{}: {}={!r} with rules={!r}, dataclass={!r}, error_handler={!r}>".format(
            self.__class__.__name__,
            "blocking function" if self.is_blocking else "function",
            self.function.__qualname__,
            self.rules,
            self.dataclass,
            self.error_handler,
        )

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return get_nodes(self.function)

    def get_func_event_param(self, event: Event) -> str | None:
        event_class = self.dataclass or event.__class__
        for k, v in get_annotations(self.function).items():
            if isinstance(v := typing.get_origin(v) or v, type) and v is event_class:
                self.func_event_param = k
                return k
        return None

    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        if self.update_type is not None and self.update_type != event.update_type:
            return False

        logger.debug("Checking handler {!r}...", self)
        ctx = Context(raw_update=event) if ctx is None else ctx
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context.copy()
        update = event

        for rule in self.rules:
            if not await check_rule(api, rule, update, temp_ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        nodes = self.required_nodes
        node_col = None
        if nodes:
            result = await compose_nodes(nodes, ctx, data={Update: event, API: api})
            if not result:
                logger.debug(f"Cannot compose nodes for handler. Error: {result.error!r}")
                return False

            node_col = result.value
            temp_ctx |= node_col.values

        logger.debug("All checks passed for handler.")
        temp_ctx["node_col"] = node_col
        ctx |= temp_ctx
        return True

    async def run(
        self,
        api: API,
        event: Event,
        ctx: Context,
        node_col: "NodeCollection | None" = None,
    ) -> typing.Any:
        logger.debug(f"Running handler {self!r}...")

        try:
            if event_param := self.get_func_event_param(event):
                ctx = Context(**{event_param: event, **ctx})
            return await self(**magic_bundle(self.function, ctx, start_idx=0))
        except BaseException as exception:
            return await self.error_handler.run(exception, event, api, ctx)
        finally:
            if node_col := ctx.node_col:
                await node_col.close_all()


__all__ = ("FuncHandler",)
