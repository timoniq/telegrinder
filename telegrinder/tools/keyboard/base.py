from __future__ import annotations

import abc
import typing

from telegrinder.tools.keyboard.abc import ABCKeyboard, ABCStaticKeyboard, AnyMarkup, DictStrAny
from telegrinder.tools.keyboard.buttons.base import BaseButton

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.buttons.base import BaseStaticButton

KEYBOARD_BUTTONS_KEY: typing.Final[str] = "_buttons"
NO_VALUE: typing.Final[object] = object()


class BaseKeyboard(ABCKeyboard, abc.ABC):
    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @abc.abstractmethod
    def get_settings(self) -> DictStrAny:
        pass

    def __or__(self, other: object, /) -> typing.Self:
        if not isinstance(other, BaseButton):
            return NotImplemented
        return self.add(other)

    def __matmul__(self, other: object, /) -> typing.Self:
        return self.__or__(other).row()


class BaseStaticKeyboard(ABCStaticKeyboard, abc.ABC):
    __max_in_row__: int

    @classmethod
    def get_buttons(cls) -> dict[str, BaseStaticButton]:
        if (buttons := cls._get_secret_value(KEYBOARD_BUTTONS_KEY)) is not NO_VALUE:
            return buttons
        return cls._set_secret_value(KEYBOARD_BUTTONS_KEY, super().get_buttons())

    @classmethod
    def _set_secret_value[V](cls, key: str, value: V, /) -> V:
        setattr(cls, key, value)
        return value

    @classmethod
    def _get_secret_value(cls, key: str, /) -> typing.Any:
        return getattr(cls, key, NO_VALUE)

    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass


__all__ = ("BaseKeyboard", "BaseStaticKeyboard")
