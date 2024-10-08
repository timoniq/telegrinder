import dataclasses
import typing
from abc import ABC, abstractmethod

from fntypes.option import Some

from telegrinder.model import is_none
from telegrinder.types.objects import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from .buttons import Button, InlineButton, KeyboardButton, RowButtons

DictStrAny: typing.TypeAlias = dict[str, typing.Any]
AnyMarkup: typing.TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


def copy_keyboard(keyboard: list[list[DictStrAny]]) -> list[list[DictStrAny]]:
    return [row.copy() for row in keyboard]


@dataclasses.dataclass(kw_only=True, slots=True)
class KeyboardModel:
    resize_keyboard: bool
    one_time_keyboard: bool
    selective: bool
    is_persistent: bool
    keyboard: list[list[DictStrAny]]


class ABCMarkup(ABC, typing.Generic[KeyboardButton]):
    BUTTON: type[KeyboardButton]
    keyboard: list[list[DictStrAny]]

    @abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @classmethod
    def get_empty_markup(cls) -> AnyMarkup:
        return cls().get_markup()

    def add(self, row_or_button: RowButtons[KeyboardButton] | KeyboardButton) -> typing.Self:
        if not len(self.keyboard):
            self.row()

        if isinstance(row_or_button, RowButtons):
            self.keyboard[-1].extend(row_or_button.get_data())
            if row_or_button.auto_row:
                self.row()
            return self

        self.keyboard[-1].append(row_or_button.get_data())
        return self

    def row(self) -> typing.Self:
        if len(self.keyboard) and not len(self.keyboard[-1]):
            return self

        self.keyboard.append([])
        return self

    def format(self, **format_data: str) -> typing.Self:
        copy_keyboard = self.__class__()
        for row in self.keyboard:
            for button in row:
                copy_button = button.copy()
                copy_button["text"] = copy_button["text"].format(**format_data)
                copy_keyboard.add(self.BUTTON(**copy_button))
            copy_keyboard.row()
        return copy_keyboard

    def merge(self, other: typing.Self) -> typing.Self:
        self.keyboard.extend(copy_keyboard(other.keyboard))
        return self


@dataclasses.dataclass(kw_only=True, slots=True)
class Keyboard(ABCMarkup[Button], KeyboardModel):
    BUTTON = Button

    keyboard: list[list[DictStrAny]] = dataclasses.field(
        default_factory=lambda: [[]],
        init=False,
    )
    resize_keyboard: bool = dataclasses.field(default=True)
    one_time_keyboard: bool = dataclasses.field(default=False)
    selective: bool = dataclasses.field(default=False)
    is_persistent: bool = dataclasses.field(default=False)

    def dict(self) -> DictStrAny:
        self.keyboard = [row for row in self.keyboard if row]
        return {
            k: v.unwrap() if v and isinstance(v, Some) else v
            for k, v in dataclasses.asdict(self).items()
            if not is_none(v)
        }

    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(**self.dict())

    def keyboard_remove(self, *, selective: bool = False) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove(remove_keyboard=True, selective=selective)


class InlineKeyboard(ABCMarkup[InlineButton]):
    BUTTON = InlineButton

    def __init__(self) -> None:
        self.keyboard = [[]]

    def dict(self) -> DictStrAny:
        self.keyboard = [row for row in self.keyboard if row]
        return dict(inline_keyboard=self.keyboard)

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(**self.dict())


__all__ = (
    "ABCMarkup",
    "InlineKeyboard",
    "Keyboard",
    "KeyboardModel",
    "copy_keyboard",
)
