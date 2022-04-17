from typing import List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .buttons import Button, InlineButton


@dataclass()
class KeyboardModel:
    resize_keyboard: bool
    one_time_keyboard: bool
    selective: bool
    keyboard: List[List[dict]]


class ABCMarkup(ABC, KeyboardModel):
    @abstractmethod
    def add(self, button) -> "ABCMarkup":
        pass

    @abstractmethod
    def row(self) -> "ABCMarkup":
        pass

    @abstractmethod
    def dict(self) -> dict:
        pass


class Keyboard(ABCMarkup):
    def __init__(
        self,
        resize_keyboard: bool = False,
        one_time_keyboard: bool = False,
        selective: Optional[bool] = None,
    ):
        self.keyboard = [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

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


class InlineKeyboard(ABCMarkup):
    keyboard: List[List[dict]] = [[]]

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
