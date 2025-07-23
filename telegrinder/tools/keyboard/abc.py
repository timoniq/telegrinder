from __future__ import annotations

import abc
import typing

from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.button import BaseButton

from telegrinder.tools.keyboard.utils import RowButtons, copy_keyboard

type DictStrAny = dict[str, typing.Any]
type AnyMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
type RawKeyboard = list[list[DictStrAny]]
type Button = DictStrAny | list[DictStrAny] | BaseButton[typing.Any] | RowButtons[BaseButton[typing.Any]]


class ABCKeyboard(typing.Protocol):
    keyboard: RawKeyboard

    __button_class__: typing.ClassVar[type[BaseButton]]

    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @abc.abstractmethod
    def copy(self, **with_changes: typing.Any) -> typing.Self:
        pass

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

    def merge(self, other: typing.Self, /) -> typing.Self:
        self.keyboard.extend(copy_keyboard(other.keyboard))
        return self

    def merge_to_last_row(self, other: typing.Self, /) -> typing.Self:
        total_rows = len(other.keyboard)

        for index, row in enumerate(copy_keyboard(other.keyboard), start=1):
            for button in row:
                self.keyboard[-1].append(button)

            if index < total_rows:
                self.keyboard.append([])

        return self


__all__ = ("ABCKeyboard",)
