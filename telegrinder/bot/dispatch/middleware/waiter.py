import datetime
import typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.modules import logger

if typing.TYPE_CHECKING:
    from telegrinder.tools.waiter_machine.hasher import Hasher
    from telegrinder.tools.waiter_machine.machine import WaiterMachine


class WaiterMiddleware(ABCMiddleware):
    def __init__(self, machine: WaiterMachine) -> None:
        self.machine = machine
        self.hashers: set[Hasher[typing.Any, typing.Any]] = set()

    def __bool__(self) -> bool:
        return bool(self.hashers) and bool(self.machine)

    def add_hasher(self, hasher: Hasher[typing.Any, typing.Any], /) -> None:
        self.hashers.add(hasher)

    async def pre(self, api: API, ctx: Context) -> bool:
        update = ctx.update_cute
        update_type = update.update_type
        event = update.incoming_update
        initiator = short_state = None

        for hasher in self.hashers:
            if hasher not in self.machine.storage or (hasher.update_types and update_type not in hasher.update_types):
                continue

            key = hasher.get_hash_from_data_from_event(event)
            if not key:
                continue

            if (
                short_state := self.machine.storage[hasher].get(key.unwrap())
            ) is not None and datetime.datetime.now() < short_state.expiration_date:
                initiator = hasher
                break

        if short_state is None or initiator is None:
            logger.debug("No state with {} hashers found", len(self.hashers))
            return True

        from telegrinder.bot.dispatch.handler.func import FuncHandler, check_rule

        if short_state.filter is not None and not await check_rule(short_state.filter, ctx):
            return True

        if await FuncHandler(
            function=lambda: short_state.release(event=event, context=ctx),
            rules=(short_state.release_rule,) if short_state.release_rule is not None else None,
            preset_context=short_state.context.context if short_state.context is not None else None,
        ).run(api, update, ctx):
            ctx.initiator = initiator
            return False

        if (on_miss := short_state.actions.get("on_miss")) is not None:
            await on_miss.run(api, update, ctx)

        return False


__all__ = ("WaiterMiddleware",)
