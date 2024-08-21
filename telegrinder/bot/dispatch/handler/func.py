import dataclasses
from functools import cached_property

import typing_extensions as typing

from telegrinder.api import API
from telegrinder.bot.cute_types import BaseCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.model import Model
from telegrinder.modules import logger
from telegrinder.node.base import Node, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.node.event import EVENT_NODE_KEY
from telegrinder.tools.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules import ABCRule

F = typing.TypeVar(
    "F",
    bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable[typing.Any]],
)
Event = typing.TypeVar("Event", bound=Model)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler)


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler(ABCHandler[Event], typing.Generic[Event, F, ErrorHandlerT]):
    func: F
    rules: list["ABCRule"]
    is_blocking: bool = dataclasses.field(default=True, kw_only=True)
    dataclass: type[typing.Any] | None = dataclasses.field(default=dict, kw_only=True)
    error_handler: ErrorHandlerT = dataclasses.field(
        default_factory=lambda: typing.cast(ErrorHandlerT, ErrorHandler()),
        kw_only=True,
    )
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)
    update_type: UpdateType | None = dataclasses.field(default=None, kw_only=True)

    def __repr__(self) -> str:
        return "<{}: {}={!r} with rules={!r}, dataclass={!r}, error_handler={!r}>".format(
            self.__class__.__name__,
            "blocking function" if self.is_blocking else "function",
            self.func.__name__,
            self.rules,
            self.dataclass,
            self.error_handler,
        )

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return get_nodes(self.func)

    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        if self.update_type is not None and self.update_type != event.update_type:
            return False

        logger.debug("Checking handler {!r}...", self)
        ctx = Context(raw_update=event) if ctx is None else ctx
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        nodes = self.required_nodes
        node_col = None
        update = event

        if nodes:
            result = await compose_nodes(nodes, ctx, data={Update: event, API: api})
            if not result:
                logger.debug(f"Cannot compose nodes for handler. {result.error}")
                return False

            node_col = result.value
            temp_ctx |= node_col.values

            if EVENT_NODE_KEY in ctx:
                for name, node in nodes.items():
                    if node is ctx[EVENT_NODE_KEY] and name in temp_ctx:
                        ctx[EVENT_NODE_KEY] = temp_ctx.pop(name)

        for rule in self.rules:
            if not await check_rule(api, rule, update, temp_ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        logger.debug("All checks passed for handler.")

        temp_ctx["node_col"] = node_col
        ctx |= temp_ctx
        return True

    async def run(self, api: API, event: Event, ctx: Context) -> typing.Any:
        logger.debug(f"Running func handler {self.func}")
        dataclass_type = typing.get_origin(self.dataclass) or self.dataclass

        if dataclass_type is Update and (event_node := ctx.pop(EVENT_NODE_KEY, None)) is not None:
            event = event_node

        elif dataclass_type is not None:
            if self.update_type is not None and isinstance(event, Update):
                update = event.to_dict()[self.update_type.value].unwrap()
                event = (
                    self.dataclass.from_update(update, bound_api=api)  # type: ignore
                    if issubclass(dataclass_type, BaseCute)
                    else self.dataclass(**update.to_dict())  # type: ignore
                )

            elif issubclass(dataclass_type, UpdateCute) and isinstance(event, Update):
                event = self.dataclass.from_update(event, bound_api=api)  # type: ignore

            else:
                event = self.dataclass(**event.to_dict())  # type: ignore

        result = (await self.error_handler.run(self.func, event, api, ctx)).unwrap()
        if node_col := ctx.node_col:
            await node_col.close_all()
        return result


__all__ = ("FuncHandler",)
