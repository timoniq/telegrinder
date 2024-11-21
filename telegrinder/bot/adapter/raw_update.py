from fntypes.result import Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.adapter.abc import ABCAdapter
from telegrinder.bot.adapter.errors import AdapterError
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    ADAPTED_VALUE_KEY: str = "_adapted_update_cute"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: adapt Update -> UpdateCute>"

    def adapt(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> Result[UpdateCute, AdapterError]:
        if self.ADAPTED_VALUE_KEY not in context:
            context[self.ADAPTED_VALUE_KEY] = (
                UpdateCute.from_update(update, api) if not isinstance(update, UpdateCute) else update
            )
        return Ok(context[self.ADAPTED_VALUE_KEY])


__all__ = ("RawUpdateAdapter",)
