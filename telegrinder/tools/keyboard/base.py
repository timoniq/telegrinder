from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.abc import Button, RawKeyboard
    from telegrinder.tools.keyboard.button import BaseButton

from telegrinder.tools.keyboard.abc import ABCKeyboard
from telegrinder.tools.keyboard.utils import RowButtons, copy_keyboard, get_keyboard_button_rules, is_dunder

BUTTON_CLASS_KEY: typing.Final[str] = "__button_class__"


class KeyboardMeta(type):
    if not typing.TYPE_CHECKING:

        def __getattribute__(cls, __name: str) -> typing.Any:
            if (
                not is_dunder(__name)
                and ABCKeyboard not in type.__getattribute__(cls, "__bases__")
                and hasattr(cls, BUTTON_CLASS_KEY)
                and (button_rule := get_keyboard_button_rules(cls).get(__name)) is not None
            ):
                return button_rule

            return super().__getattribute__(__name)


class ABCBaseKeyboard(typing._ProtocolMeta, KeyboardMeta):  # type: ignore
    pass


class BaseKeyboard[KeyboardButton: BaseButton = typing.Any](typing.Protocol, metaclass=ABCBaseKeyboard):
    keyboard: RawKeyboard

    __keyboard_instance__: typing.ClassVar[typing.Self]
    __button_class__: typing.ClassVar[type[BaseButton[typing.Self]]]

    @abc.abstractmethod
    def copy(self, **with_changes: typing.Any) -> typing.Self:
        pass

    @abc.abstractmethod
    def __init_subclass__(cls) -> None:
        pass

    def __and__(self, other: object, /) -> typing.Self:
        if not isinstance(other, self.__button_class__ | type(self)):
            return NotImplemented
        return self.add(other) if isinstance(other, self.__button_class__) else self.merge(other)  # type: ignore

    def __or__(self, other: object, /) -> typing.Self:
        if not isinstance(other, self.__button_class__ | type(self)):
            return NotImplemented
        kb = self.row()
        return kb.add(other) if isinstance(other, self.__button_class__) else kb.merge_to_last_row(other)  # type: ignore

    def add(self, button: Button, /) -> typing.Self:
        if not self.keyboard:
            self.row()

        if isinstance(button, RowButtons):
            self.keyboard[-1].extend(button.get_data())
            if button.auto_row:
                self.row()
            return self

        if isinstance(button, list):
            self.keyboard[-1].extend(button)
            return self

        self.keyboard[-1].append(button if isinstance(button, dict) else button.get_data())
        return self

    def row(self) -> typing.Self:
        if len(self.keyboard) and not len(self.keyboard[-1]):
            return self

        self.keyboard.append([])
        return self

    def format_text(self, **format_data: typing.Any) -> typing.Self:
        copy_keyboard = self.copy()

        for row in self.keyboard:
            for button in row:
                button.update(dict(text=button["text"].format(**format_data)))

        return copy_keyboard

    def merge(self, other: BaseKeyboard[KeyboardButton], /) -> typing.Self:
        self.keyboard.extend(copy_keyboard(other.keyboard))
        return self

    def merge_to_last_row(self, other: BaseKeyboard[KeyboardButton], /) -> typing.Self:
        total_rows = len(other.keyboard)

        for index, row in enumerate(copy_keyboard(other.keyboard), start=1):
            for button in row:
                self.keyboard[-1].append(button)

            if index < total_rows:
                self.keyboard.append([])

        return self


__all__ = ("BaseKeyboard",)
