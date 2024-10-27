from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.return_manager.pre_checkout_query import PreCheckoutQueryManager
from telegrinder.bot.dispatch.view.base import BaseStateView


class PreCheckoutQueryView(BaseStateView[PreCheckoutQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = PreCheckoutQueryManager()

    def get_state_key(self, event: PreCheckoutQueryCute) -> int | None:
        return event.from_user.id


__all__ = ("PreCheckoutQueryView",)
