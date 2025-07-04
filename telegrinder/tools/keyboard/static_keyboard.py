from __future__ import annotations

import dataclasses
import typing

from telegrinder.tools.keyboard.abc import DictStrAny
from telegrinder.tools.keyboard.base import BaseStaticKeyboard
from telegrinder.tools.keyboard.data import KeyboardModel
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

type RawKeyboard = typing.Iterable[typing.Iterable[DictStrAny]]


def create_keyboard(cls_: type[BaseStaticKeyboard], /) -> RawKeyboard:
    buttons = cls_.get_buttons()
    max_in_row = cls_.__max_in_row__
    keyboard = [[]]

    for button in buttons.values():
        keyboard[-1].append(button.get_data())

        if (button.row is True or len(keyboard[-1]) >= max_in_row) and keyboard[-1]:
            keyboard.append([])

    return tuple(tuple(x) for x in keyboard if x)


class StaticKeyboard(BaseStaticKeyboard):
    __keyboard__: KeyboardModel

    def __init_subclass__(
        cls,
        *,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
        is_persistent: bool = False,
        input_field_placeholder: str | None = None,
        max_in_row: int = 3,
    ) -> None:
        cls.__max_in_row__ = max_in_row
        cls.__keyboard__ = KeyboardModel(
            keyboard=create_keyboard(cls),
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            is_persistent=is_persistent,
            input_field_placeholder=input_field_placeholder,
        )

    @classmethod
    def dict(cls) -> DictStrAny:
        return dataclasses.asdict(cls.__keyboard__)

    @classmethod
    def get_markup(cls) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup.from_dict(cls.dict())

    @classmethod
    def get_keyboard_remove(cls) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove.from_data(
            remove_keyboard=True,
            selective=cls.__keyboard__.selective,
        )


class StaticInlineKeyboard(BaseStaticKeyboard):
    __keyboard__: RawKeyboard

    def __init_subclass__(cls, *, max_in_row: int = 3) -> None:
        cls.__max_in_row__ = max_in_row
        cls.__keyboard__ = create_keyboard(cls)

    @classmethod
    def dict(cls) -> DictStrAny:
        return dict(inline_keyboard=cls.__keyboard__)

    @classmethod
    def get_markup(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup.from_dict(cls.dict())


__all__ = ("StaticInlineKeyboard", "StaticKeyboard")
