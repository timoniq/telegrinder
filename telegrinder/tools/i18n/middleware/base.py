from abc import abstractmethod

from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.tools.i18n import ABCI18n
from telegrinder.tools.i18n.constants import I18N_KWARG_NAME


class ABCTranslatorMiddleware(ABCMiddleware):
    def __init__(self, i18n: ABCI18n):
        self.i18n = i18n

    @abstractmethod
    async def get_locale(self, event) -> str:
        pass

    async def pre(self, event, ctx: dict) -> bool:
        ctx[I18N_KWARG_NAME] = self.i18n.get_translator_by_locale(await self.get_locale(event))
        return True
