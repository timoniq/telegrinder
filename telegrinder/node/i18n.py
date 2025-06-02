import abc
import dataclasses
import gettext
import os
import pathlib
import typing
from functools import cached_property

from telegrinder.node.base import DataNode, GlobalNode
from telegrinder.node.source import Locale

type Separator = KeySeparator

DEFAULT_SEPARATOR: typing.Final[str] = "-"


@dataclasses.dataclass(frozen=True)
class KeySeparator(GlobalNode[Separator], DataNode):
    value: str

    @classmethod
    def set(cls, value: str, /) -> None:
        super().set(cls(value))

    @classmethod
    def compose(cls) -> Separator:
        return cls.get(default=cls(DEFAULT_SEPARATOR))


@dataclasses.dataclass(kw_only=True)
class ABCTranslator(DataNode, abc.ABC):
    locale: str
    separator: str
    _keys: list[str] = dataclasses.field(default_factory=list[str], init=False)

    @typing.overload
    def __call__(self, **context: typing.Any) -> str: ...

    @typing.overload
    def __call__(self, message_id: str, /, **context: typing.Any) -> str: ...

    def __call__(self, message_id: str | None = None, **context: typing.Any) -> str:
        result = self.translate(message_id or self.message_id, **context)
        if not message_id:
            self._keys.clear()
        return result

    def __getattr__(self, __key: str) -> typing.Self:
        self._keys.append(__key)
        return self

    @property
    def message_id(self) -> str:
        return self.separator.join(self._keys)

    @abc.abstractmethod
    def translate(self, message_id: str, **context: typing.Any) -> str:
        pass

    @classmethod
    def compose(cls, locale: Locale, separator: KeySeparator) -> typing.Self:
        return cls(locale=locale, separator=separator.value)


@dataclasses.dataclass
class I18NConfig:
    domain: str
    folder: str | pathlib.Path
    default_locale: str = dataclasses.field(default="en")

    @cached_property
    def translators(self) -> dict[str, gettext.GNUTranslations]:
        result = {}

        for name in os.listdir(self.folder):
            if not os.path.isdir(os.path.join(self.folder, name)):
                continue

            mo_path = os.path.join(self.folder, name, "LC_MESSAGES", f"{self.domain}.mo")

            if os.path.exists(mo_path):
                with open(mo_path, "rb") as f:
                    result[name] = gettext.GNUTranslations(f)
            elif os.path.exists(mo_path[:-2] + "po"):
                raise FileNotFoundError(".po files should be compiled first")

        return result

    def get_translator(self, locale: str, /) -> gettext.GNUTranslations:
        locale = locale if locale in self.translators else self.default_locale
        return self.translators[locale]


class BaseTranslator(ABCTranslator):
    config: typing.ClassVar[I18NConfig]

    def __class_getitem__(cls, config: I18NConfig, /) -> typing.Any:
        return type(cls.__name__, (cls,), dict(config=config))

    @classmethod
    def configure(cls, config: I18NConfig, /) -> None:
        cls.config = config

    def translate(self, message_id: str, **context: typing.Any) -> str:
        return self.config.get_translator(self.locale).gettext(message_id).format(**context)


__all__ = ("ABCTranslator", "BaseTranslator", "I18NConfig", "KeySeparator")
