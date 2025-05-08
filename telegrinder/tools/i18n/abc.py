from __future__ import annotations

import enum
import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule

TRANSLATIONS_KEY: typing.Final[str] = "_translations"


def get_cached_translation[Rule: ABCRule](rule: Rule, locale: str) -> Rule | None:
    return getattr(rule, TRANSLATIONS_KEY, {}).get(locale)


def cache_translation[Rule: ABCRule](
    base_rule: Rule,
    locale: str,
    translated_rule: Rule,
) -> None:
    translations = getattr(base_rule, TRANSLATIONS_KEY, {})
    translations[locale] = translated_rule
    setattr(base_rule, TRANSLATIONS_KEY, translations)


class ABCI18n(ABC):
    @abstractmethod
    def get_translator_by_locale(self, locale: str) -> "ABCTranslator":
        pass


class ABCTranslator(ABC):
    def __init__(self, locale: str, **kwargs: typing.Any) -> None:
        self.locale = locale

    @abstractmethod
    def get(self, __key: str, *args: typing.Any, **kwargs: typing.Any) -> str:
        """This translates a key to actual human-readable string"""

    def __call__(self, __key: str, *args: typing.Any, **kwargs: typing.Any) -> str:
        return self.get(__key, *args, **kwargs)


class I18nEnum(enum.Enum):
    I18N = "_"


__all__ = ("ABCI18n", "ABCTranslator", "I18nEnum")
