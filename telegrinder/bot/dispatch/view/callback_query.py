from telegrinder.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType


class CallbackQueryView(BaseView):
    def __init__(self) -> None:
        super().__init__(UpdateType.CALLBACK_QUERY)
        self.return_manager = CallbackQueryReturnManager()


__all__ = ("CallbackQueryView",)
