from telegrinder.bot.dispatch.return_manager.pre_checkout_query import PreCheckoutQueryManager
from telegrinder.bot.dispatch.view.base import BaseView
from telegrinder.types.enums import UpdateType


class PreCheckoutQueryView(BaseView):
    def __init__(self) -> None:
        super().__init__(UpdateType.PRE_CHECKOUT_QUERY)
        self.return_manager = PreCheckoutQueryManager()


__all__ = ("PreCheckoutQueryView",)
