from __future__ import annotations

import dataclasses
import typing

from telegrinder.tools.keyboard.abc import ABCStaticKeyboard, DictStrAny
from telegrinder.tools.keyboard.buttons.base import BaseStaticButton
from telegrinder.tools.keyboard.data import KeyboardModel
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

type RawKeyboard = typing.Iterable[typing.Iterable[DictStrAny]]

KEYBOARD_BUTTONS_KEY: typing.Final[str] = "_buttons"
NO_VALUE: typing.Final[object] = object()


def create_keyboard(cls_: type[BaseStaticKeyboard], /) -> RawKeyboard:
    buttons = cls_.get_buttons()
    max_in_row = cls_.__max_in_row__
    keyboard = [[]]

    for button in buttons.values():
        keyboard[-1].append(button.get_data())

        if (button.row is True or len(keyboard[-1]) >= max_in_row) and keyboard[-1]:
            keyboard.append([])

    return tuple(tuple(x) for x in keyboard if x)


class BaseStaticKeyboard(ABCStaticKeyboard):
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


class StaticKeyboard(BaseStaticKeyboard):
    __keyboard__: KeyboardModel

    def __init_subclass__(
        cls,
        *,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
        is_persistent: bool = False,
        max_in_row: int = 3,
    ) -> None:
        cls.__max_in_row__ = max_in_row
        cls.__keyboard__ = KeyboardModel(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            is_persistent=is_persistent,
            keyboard=create_keyboard(cls),
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


__all__ = ("BaseStaticKeyboard", "StaticInlineKeyboard", "StaticKeyboard")
