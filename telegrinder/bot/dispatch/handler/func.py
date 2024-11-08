import dataclasses
from functools import cached_property

import typing_extensions as typing

from telegrinder.api.api import API
from telegrinder.bot.cute_types import BaseCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.model import Model
from telegrinder.modules import logger
from telegrinder.node.base import Node, get_nodes
from telegrinder.node.composer import NodeCollection, compose_nodes
from telegrinder.node.event import EVENT_NODE_KEY
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.node.composer import NodeCollection

Function = typing.TypeVar("Function", bound="Func[..., typing.Any]")
Event = typing.TypeVar("Event", bound=Model)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)

type Func[**Rest, Result] = typing.Callable[Rest, typing.Coroutine[typing.Any, typing.Any, Result]]


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler(ABCHandler[Event], typing.Generic[Event, Function, ErrorHandlerT]):
    function: Function
    rules: list["ABCRule"]
    is_blocking: bool = dataclasses.field(default=True, kw_only=True)
    dataclass: type[typing.Any] | None = dataclasses.field(default=dict, kw_only=True)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast(ErrorHandlerT, ErrorHandler()),
        kw_only=True,
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)
    update_type: UpdateType | None = dataclasses.field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        self.dataclass = typing.get_origin(self.dataclass) or self.dataclass

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

            if EVENT_NODE_KEY in ctx:
                for name, node in nodes.items():
                    if node is ctx[EVENT_NODE_KEY] and name in temp_ctx:
                        ctx[name] = temp_ctx.pop(name)

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
        logger.debug(f"Running func handler {self.function.__qualname__!r}")

        if self.dataclass is not None and EVENT_NODE_KEY not in ctx:
            if self.update_type is not None and isinstance(event, Update):
                update = getattr(event, event.update_type.value).unwrap()
                event = (
                    self.dataclass.from_update(update, bound_api=api)
                    if issubclass(self.dataclass, BaseCute)
                    else self.dataclass(**update.to_dict())  # type: ignore
                )

            elif issubclass(self.dataclass, UpdateCute) and isinstance(event, Update):
                event = self.dataclass.from_update(event, bound_api=api)

            else:
                event = self.dataclass(**event.to_dict())  # type: ignore

        result = (await self.error_handler.run(self.function, event, api, ctx)).unwrap()
        if node_col := ctx.node_col:
            await node_col.close_all()
        return result


__all__ = ("FuncHandler",)
