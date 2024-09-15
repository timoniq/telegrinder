import enum
import typing
from abc import ABC, abstractmethod


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


__all__ = (
    "ABCI18n",
    "ABCTranslator",
    "I18nEnum",
)
