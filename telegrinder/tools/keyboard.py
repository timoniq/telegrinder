import typing
from typing import List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup

from .buttons import Button, InlineButton


AnyMarkup = typing.Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]


@dataclass()
class KeyboardModel:
    resize_keyboard: bool
    one_time_keyboard: bool
    selective: bool
    keyboard: List[List[dict]]


class ABCMarkup(ABC, KeyboardModel):
    BUTTON: typing.Any

    def __init__(
        self,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: Optional[bool] = None,
    ):
        self.keyboard = [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

    @abstractmethod
    def add(self, button) -> "ABCMarkup":
        pass

    @abstractmethod
    def row(self) -> "ABCMarkup":
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


class Keyboard(ABCMarkup):
    BUTTON = Button

    def row(self) -> "Keyboard":
        if len(self.keyboard) and not len(self.keyboard[-1]):
            raise RuntimeError("Last row is empty!")

        self.keyboard.append([])
        return self

    def add(self, button: Button) -> "Keyboard":
        if not len(self.keyboard):
            self.row()

        self.keyboard[-1].append(button.get_data())
        return self

    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(**self.dict())


class InlineKeyboard(ABCMarkup):
    BUTTON = InlineButton

    def row(self) -> "InlineKeyboard":
        if len(self.keyboard) and not len(self.keyboard[-1]):
            raise RuntimeError("Last row is empty!")

        self.keyboard.append([])
        return self

    def add(self, button: InlineButton) -> "InlineKeyboard":
        if not len(self.keyboard):
            self.row()

        self.keyboard[-1].append(button.get_data())
        return self

    def dict(self) -> dict:
        return dict(inline_keyboard=self.keyboard)

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(**self.dict())
