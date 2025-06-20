from __future__ import annotations

import dataclasses
import typing
from collections import deque
from functools import cached_property

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

type Function = typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, typing.Any]]


@dataclasses.dataclass(repr=False, slots=True)
class FuncHandler[T: Function](ABCHandler):
    function: T
    rules: dataclasses.InitVar[typing.Iterable[ABCRule] | None] = None
    final: bool = dataclasses.field(default=True, kw_only=True)
    preset_context: Context = dataclasses.field(default_factory=lambda: Context(), kw_only=True)

    def __post_init__(self, rules: typing.Iterable[ABCRule] | None) -> None:
        self.check_rules = deque(rules or ())

    @property
    def __call__(self) -> Function:
        return self.function

    def __repr__(self) -> str:
        return fullname(self.function)

    @cached_property
    def required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.function)

    async def run(
        self,
        api: API,
        event: Update,
        context: Context,
        check: bool = True,
    ) -> Result[typing.Any, str]:
        logger.debug("Checking rules and composing nodes for handler `{!r}`...", self)

        temp_ctx = context.copy()
        temp_ctx |= self.preset_context.copy()

        if check:
            for rule in self.check_rules:
                if not await check_rule(api, rule, event, temp_ctx):
                    return Error(f"Rule {rule!r} failed.")

        context |= temp_ctx
        node_col = None

        if self.required_nodes:
            match await compose_nodes(self.required_nodes, context, data={Update: event, API: api}):
                case Ok(value):
                    node_col = value
                case Error(compose_error):
                    return Error(f"Cannot compose nodes for handler `{self}`, error: {compose_error.message}")

        logger.debug("All good, running handler `{!r}`", self)

        try:
            data_bundle = bundle(
                self.function,
                {API: api, Update: event, Context: context.copy()},
                typebundle=True,
                start_idx=0,
            )
            return Ok(
                await bundle(self.function, context | ({} if node_col is None else node_col.values), start_idx=0)(
                    *data_bundle.args,
                    **data_bundle.kwargs,
                ),
            )
        finally:
            if node_col is not None:
                await node_col.close_all()


__all__ = ("FuncHandler",)
