from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.result import Ok, Result
from telegrinder.types.objects import Update


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    async def adapt(
        self,
        api: ABCAPI,
        update: Update,
    ) -> Result[UpdateCute, AdapterError]:
        if not isinstance(update, UpdateCute):
            return Ok(UpdateCute.from_update(update, api))
        return Ok(update)


__all__ = ("RawUpdateAdapter",)
