from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.types.objects import Update
from telegrinder.api import API


class ErrorView(BaseView[UpdateCute]):

    async def process(self, event: Update, api: API, context: Context) -> bool:
        return await process_inner(
            api,
            UpdateCute.from_update(event, bound_api=api),
            event,
            context,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )
