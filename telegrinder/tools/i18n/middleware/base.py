from abc import abstractmethod

from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.tools.i18n import ABCI18n


class ABCTranslatorMiddleware(ABCMiddleware):
    def __init__(self, i18n: ABCI18n, kwarg_name: str = "_"):
        self.i18n = i18n
        self.kwarg_name = kwarg_name

    @abstractmethod
    async def get_locale(self, event) -> str:
        pass

    async def pre(self, event, ctx: dict) -> bool:
        ctx[self.kwarg_name] = self.i18n.get_translator_by_locale(await self.get_locale(event))
        return True
