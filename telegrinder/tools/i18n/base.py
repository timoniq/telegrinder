from abc import ABC, abstractmethod


class ABCI18n(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_translator_by_locale(self, locale: str) -> "ABCTranslator":
        pass


class ABCTranslator(ABC):
    def __init__(self, locale: str, **kwargs):
        self.locale = locale

    @abstractmethod
    def get(self, key: str, **kwargs) -> str:
        """This translates a key to actual human-readable string"""

    def __call__(self, key: str, **kwargs):
        return self.get(key, **kwargs)
