"""This is an implementation of GNU gettext (pyBabel)."""
import gettext
import os

from telegrinder.tools.i18n import ABCI18n
from telegrinder.tools.i18n.base import ABCTranslator


class SimpleI18n(ABCI18n):
    def __init__(self, folder: str, domain: str, default_locale: str):
        self.folder = folder
        self.domain = domain
        self.default_locale = default_locale
        self.translators = self._load_translators()

    def _load_translators(self) -> dict[str, gettext.GNUTranslations]:
        result = {}
        for name in os.listdir(self.folder):
            if not os.path.isdir(os.path.join(self.folder, name)):
                continue

            mo_path = os.path.join(
                self.folder, name, "LC_MESSAGES", f"{self.domain}.mo"
            )
            if os.path.exists(mo_path):
                with open(mo_path, "rb") as f:
                    result[name] = gettext.GNUTranslations(f)
            elif os.path.exists(mo_path[:-2] + "po"):
                raise FileNotFoundError(".po files should be compiled first")
        return result

    def get_translator_by_locale(self, locale: str) -> "SimpleTranslator":
        return SimpleTranslator(
            locale, self.translators.get(locale, self.translators[self.default_locale])
        )


class SimpleTranslator(ABCTranslator):
    def __init__(self, locale: str, g: gettext.GNUTranslations):
        self.g = g
        super().__init__(locale)

    def get(self, key: str, **kwargs) -> str:
        return self.g.gettext(key).format(**kwargs)
