import dataclasses
import typing
from abc import ABC, abstractmethod

from telegrinder.option import Nothing, Some
from telegrinder.option.msgspec_option import Option
from telegrinder.types.methods import OptionType
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from .buttons import BaseButton, Button, InlineButton

AnyMarkup = InlineKeyboardMarkup | ReplyKeyboardMarkup


def keyboard_remove(selective: bool | None = None) -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove(
        remove_keyboard=True,
        selective=Option.Nothing if selective is None else Option(selective),
    )


@dataclasses.dataclass
class KeyboardModel:
    resize_keyboard: bool | OptionType[bool]
    one_time_keyboard: bool | OptionType[bool]
    selective: bool | OptionType[bool]
    keyboard: list[list[dict]]


class ABCMarkup(ABC, KeyboardModel):
    BUTTON: type[BaseButton]

    def __init__(
        self,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
    ):
        self.keyboard = [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

    @abstractmethod
    def add(self, button) -> typing.Self:
        pass

    @abstractmethod
    def row(self) -> typing.Self:
        pass

    @abstractmethod
    def dict(self) -> dict:
        pass

    @abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @classmethod
    def empty(cls) -> AnyMarkup:
        return cls().get_markup()

    def format(self, **format_data: typing.Dict[str, str]) -> "ABCMarkup":
        copy_keyboard = self.__class__()
        for row in self.keyboard:
            for button in row:
                copy_button = button.copy()
                copy_button["text"] = copy_button["text"].format(**format_data)
                copy_keyboard.add(self.BUTTON(**copy_button))
            copy_keyboard.row()
        return copy_keyboard

    def merge(self, other: typing.Self) -> typing.Self:
        self.keyboard.extend(other.keyboard)
        return self


class Keyboard(ABCMarkup):
    BUTTON = Button

    def row(self) -> "Keyboard":
        if len(self.keyboard) and not len(self.keyboard[-1]):
            raise RuntimeError("Last row is empty!")

        self.keyboard.append([])
        return self

    def add(self, button: Button) -> typing.Self:
        if not len(self.keyboard):
            self.row()

        self.keyboard[-1].append(button.get_data())
        return self

    def dict(self) -> dict:
        return {
            k: v.unwrap() if v and isinstance(v, Option | Some) else v
            for k, v in self.__dict__.items()
            if v not in (None, Nothing)
        }

    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(**self.dict())


class InlineKeyboard(ABCMarkup):
    BUTTON = InlineButton

    def row(self) -> typing.Self:
        if len(self.keyboard) and not len(self.keyboard[-1]):
            raise RuntimeError("Last row is empty!")

        self.keyboard.append([])
        return self

    def add(self, button: InlineButton) -> typing.Self:
        if not len(self.keyboard):
            self.row()

        self.keyboard[-1].append(button.get_data())
        return self

    def dict(self) -> dict:
        return dict(inline_keyboard=self.keyboard)

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(**self.dict())
