from fntypes.result import Ok, Result

from telegrinder.api.abc import ABCAPI
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.adapter.abc import ABCAdapter
from telegrinder.bot.rules.adapter.errors import AdapterError
from telegrinder.types.objects import Update


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    ADAPTED_VALUE_KEY: str = "_adapted_update_cute"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: adapt Update -> UpdateCute>"

    async def adapt(
        self,
        api: ABCAPI,
        update: Update,
        context: Context,
    ) -> Result[UpdateCute, AdapterError]:
        if self.ADAPTED_VALUE_KEY not in context:
            context[self.ADAPTED_VALUE_KEY] = (
                UpdateCute.from_update(update, api)
                if not isinstance(update, UpdateCute)
                else update
            )
        return Ok(context[self.ADAPTED_VALUE_KEY])


__all__ = ("RawUpdateAdapter",)
