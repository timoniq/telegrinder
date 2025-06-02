from telegrinder.bot.dispatch.return_manager import InlineQueryReturnManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType


class InlineQueryView(BaseView):
    def __init__(self) -> None:
        super().__init__(UpdateType.INLINE_QUERY)
        self.return_manager = InlineQueryReturnManager()


__all__ = ("InlineQueryView",)
