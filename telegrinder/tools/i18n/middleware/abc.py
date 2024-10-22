from abc import abstractmethod

from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware import ABCMiddleware
from telegrinder.tools.i18n import ABCI18n, I18nEnum


class ABCTranslatorMiddleware[Event: BaseCute](ABCMiddleware[Event]):
    def __init__(self, i18n: ABCI18n) -> None:
        self.i18n = i18n

    @abstractmethod
    async def get_locale(self, event: Event) -> str:
        pass

    async def pre(self, event: Event, ctx: Context) -> bool:
        ctx[I18nEnum.I18N] = self.i18n.get_translator_by_locale(await self.get_locale(event))
        return True


__all__ = ("ABCTranslatorMiddleware",)
