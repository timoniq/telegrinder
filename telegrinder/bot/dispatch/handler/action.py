import dataclasses
import typing
from functools import cached_property

from fntypes.misc import is_err
from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.aio import maybe_awaitable
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

type ActionResult = Result[typing.Any, typing.Any]
type Behavior = typing.Callable[..., typing.Awaitable[None] | None]
type Filter = ABCRule
type When = typing.Literal["before", "after"]


async def run_behavior(
    behavior: Behavior,
    api: API,
    update: Update,
    context: Context,
    nodes: dict[str, IsNode] | None = None,
    /,
) -> Result[None, str]:
    data = {API: api, Update: update}
    node_col = None

    if nodes:
        match await compose_nodes(nodes, context, data=data):
            case Ok(value):
                node_col = value
            case Error(compose_error):
                return Error(
                    "Cannot compose nodes for action behavior `{}`, error: {}".format(
                        fullname(behavior),
                        compose_error.message,
                    ),
                )

    try:
        data_bundle = bundle(behavior, {**data, Context: context.copy()}, start_idx=0)
        await maybe_awaitable(
            bundle(behavior, context | ({} if node_col is None else node_col.values), start_idx=0)(
                *data_bundle.args,
                **data_bundle.kwargs,
            ),
        )
        return Ok(None)
    finally:
        if node_col is not None:
            await node_col.close_all()


@dataclasses.dataclass(slots=True)
class ActionHandler(ABCHandler):
    handler: ABCHandler
    behavior: Behavior
    when: When
    filter: Filter | None = dataclasses.field(default=None)

    def __post_init__(self) -> None:
        self._runners_when = {
            "before": self.run_before,
            "after": self.run_after,
        }

    @cached_property
    def requires_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.behavior)

    async def check(self, api: API, update: Update, context: Context, /) -> bool:
        return self.filter is None or await check_rule(api, self.filter, update, context)

    async def run_before(
        self,
        api: API,
        update: Update,
        context: Context,
        check: bool,
        /,
    ) -> ActionResult:
        if is_err(
            result := await run_behavior(self.behavior, api, update, context, self.requires_nodes),
        ):
            return result

        if check and not await self.check(api, update, context):
            return Error(f"Action's filter {self.filter!r} failed!")

        return await self.handler.run(api, update, context, check)

    async def run_after(
        self,
        api: API,
        update: Update,
        context: Context,
        check: bool,
        /,
    ) -> ActionResult:
        if check and not await self.check(api, update, context):
            return Error(f"Action's filter {self.filter!r} failed!")

        handler_result = await self.handler.run(api, update, context, check)
        if is_err(handler_result):
            return handler_result

        match await run_behavior(self.behavior, api, update, context, self.requires_nodes):
            case Error(error):
                logger.debug(
                    "Cannot run action's behavior `{}`, error: {!r}",
                    fullname(self.behavior),
                    error,
                )

        return handler_result

    async def run(
        self,
        api: API,
        event: Update,
        context: Context,
        check: bool = True,
    ) -> ActionResult:
        return await self._runners_when[self.when](api, event, context, check)


__all__ = ("ActionHandler",)
