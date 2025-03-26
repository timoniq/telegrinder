from __future__ import annotations

import abc
import typing

from telegrinder.tools.keyboard.buttons.base import BaseButton, BaseStaticButton
from telegrinder.tools.keyboard.buttons.tools import RowButtons
from telegrinder.tools.repr import fullname

if typing.TYPE_CHECKING:
    from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup

type DictStrAny = dict[str, typing.Any]
type AnyMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
type RawKeyboard = list[list[DictStrAny]]
type Button[T] = DictStrAny | BaseButton | RowButtons[BaseButton]

KEYBOARD_BUTTON_CLASS_KEY: typing.Final[str] = "_button_class"
NO_VALUE: typing.Final[object] = object()


def _has_under(name: str, /) -> bool:
    return name.startswith("_")


def _get_buttons(cls_: type[ABCStaticKeyboard], /) -> dict[str, BaseStaticButton]:
    button_class = cls_.get_button_class()
    return {k: v for k, v in dict(vars(cls_)).items() if isinstance(v, button_class)}


def copy_keyboard(keyboard: RawKeyboard, /) -> RawKeyboard:
    return [row.copy() for row in keyboard]


class ABCKeyboard(abc.ABC):
    keyboard: RawKeyboard

    type Keyboard = typing.Self

    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @abc.abstractmethod
    def get_settings(self) -> DictStrAny:
        pass

    def add(self, button: Button[Keyboard], /) -> typing.Self:
        if not self.keyboard:
            self.row()

        if isinstance(button, RowButtons):
            self.keyboard[-1].extend(button.get_data())
            if button.auto_row:
                self.row()
            return self

        self.keyboard[-1].append(button if isinstance(button, dict) else button.get_data())
        return self

    def row(self) -> typing.Self:
        if len(self.keyboard) and not len(self.keyboard[-1]):
            return self

        self.keyboard.append([])
        return self

    def format_text(self, **format_data: str) -> typing.Self:
        copy_keyboard = self.__class__(**self.get_settings())

        for row in self.keyboard:
            for button in row:
                copy_button = button.copy()
                copy_button["text"] = copy_button["text"].format(**format_data)
                copy_keyboard.add(copy_button)

            copy_keyboard.row()

        return copy_keyboard

    def merge(self, other: typing.Self, /) -> typing.Self:
        self.keyboard.extend(copy_keyboard(other.keyboard))
        return self


class StaticKeyboardMeta(type):
    if not typing.TYPE_CHECKING:

        def __getattr__(cls, name, /):
            if not _has_under(name):
                buttons = _get_buttons(cls)
                if name in buttons:
                    return buttons[name]
            return super().__getattribute__(name)

    def __setattr__(cls, name: str, value: typing.Any, /) -> None:
        if not _has_under(name) and name in _get_buttons(cls):  # type: ignore
            raise AttributeError(f"Cannot reassing attribute {name!r}.")
        return super().__setattr__(name, value)

    def __delattr__(cls, name: str, /) -> None:
        if not _has_under(name) and name in _get_buttons(cls):  # type: ignore
            raise AttributeError(f"Cannot delete attribute {name!r}.")
        return super().__delattr__(name)


class ABCStaticKeyboardMeta(abc.ABCMeta, StaticKeyboardMeta):
    pass


class ABCStaticKeyboard(metaclass=ABCStaticKeyboardMeta):
    __keyboard__: typing.Any

    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @classmethod
    def get_button_class(cls) -> type[BaseStaticButton]:
        sentinel = object()
        button_class = getattr(cls, KEYBOARD_BUTTON_CLASS_KEY, sentinel)

        if button_class not in (sentinel, NO_VALUE):
            return typing.cast("type[BaseStaticButton]", button_class)

        if button_class is not NO_VALUE:
            for obj in cls.__dict__.values():
                if isinstance(obj, BaseStaticButton):
                    button_class = type(obj)
                    setattr(cls, KEYBOARD_BUTTON_CLASS_KEY, button_class)
                    return button_class

        setattr(cls, KEYBOARD_BUTTON_CLASS_KEY, NO_VALUE)
        raise ValueError(f"Static keyboard {fullname(cls)!r} has no static buttons.")

    @classmethod
    def get_buttons(cls) -> dict[str, BaseStaticButton]:
        return _get_buttons(cls)


__all__ = ("ABCKeyboard", "ABCStaticKeyboard", "copy_keyboard")
