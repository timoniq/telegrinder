from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.types.objects import Update
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.result import Result
from telegrinder.api.abc import ABCAPI


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    async def adapt(
        self, api: ABCAPI, update: Update
    ) -> Result[UpdateCute, AdapterError]:
        return Result(True, value=update)
