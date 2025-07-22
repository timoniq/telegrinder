import dataclasses
import typing

from telegrinder.tools.keyboard.abc import ABCKeyboard, DictStrAny, RawKeyboard
from telegrinder.tools.keyboard.base import BaseKeyboard
from telegrinder.tools.keyboard.button import Button, InlineButton
from telegrinder.tools.keyboard.data import KeyboardModel, KeyboardParams
from telegrinder.tools.keyboard.utils import (
    bound_keyboard_method,
    copy_keyboard,
    init_keyboard,
)
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove


class Keyboard(BaseKeyboard[Button], ABCKeyboard):
    __button_class__ = Button
    __slots__ = ("keyboard_model",)

    def __init_subclass__(cls, *, max_in_row: int = 0, **kwargs: typing.Unpack[KeyboardParams]) -> None:
        cls.__keyboard_instance__ = init_keyboard(cls(**kwargs), max_in_row=max_in_row)

    def __init__(
        self,
        *,
        keyboard_model: KeyboardModel | None = None,
        **kwargs: typing.Unpack[KeyboardParams],
    ) -> None:
        self.keyboard_model = keyboard_model or KeyboardModel(keyboard=[[]], **kwargs)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: keyboard_model={self.keyboard_model!r}>"

    @property
    def keyboard(self) -> RawKeyboard:
        return self.keyboard_model.keyboard

    @property
    def is_persistent(self) -> bool:
        return self.keyboard_model.is_persistent

    @property
    def one_time_keyboard(self) -> bool:
        return self.keyboard_model.one_time_keyboard

    @property
    def resize_keyboard(self) -> bool:
        return self.keyboard_model.resize_keyboard

    @property
    def is_selective(self) -> bool:
        return self.keyboard_model.is_selective

    @property
    def input_field_placeholder(self) -> str | None:
        return self.keyboard_model.input_field_placeholder

    @bound_keyboard_method
    def copy(self, **with_changes: typing.Any) -> typing.Self:
        keyboard_model = dataclasses.replace(
            self.keyboard_model,
            keyboard=copy_keyboard(self.keyboard),
            **with_changes,
        )
        return type(self)(keyboard_model=keyboard_model)

    @bound_keyboard_method
    def dict(self) -> DictStrAny:
        return self.keyboard_model.dict()

    @bound_keyboard_method
    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup.from_dict(self.dict())

    @bound_keyboard_method
    def get_keyboard_remove(self) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove(remove_keyboard=True, selective=self.is_selective)

    def placeholder(self, value: str | None, /) -> typing.Self:
        return self.copy(input_field_placeholder=value)

    def resize(self) -> typing.Self:
        return self.copy(resize_keyboard=True)

    def one_time(self) -> typing.Self:
        return self.copy(one_time_keyboard=True)

    def selective(self) -> typing.Self:
        return self.copy(is_selective=True)

    def persistent(self) -> typing.Self:
        return self.copy(is_persistent=True)

    def no_resize(self) -> typing.Self:
        return self.copy(resize_keyboard=False)

    def no_one_time(self) -> typing.Self:
        return self.copy(one_time_keyboard=False)

    def no_selective(self) -> typing.Self:
        return self.copy(is_selective=False)

    def no_persistent(self) -> typing.Self:
        return self.copy(is_persistent=False)


class InlineKeyboard(BaseKeyboard[InlineButton], ABCKeyboard):
    __button_class__ = InlineButton
    __slots__ = ("keyboard",)

    def __init_subclass__(cls, *, max_in_row: int = 0) -> None:
        cls.__keyboard_instance__ = init_keyboard(cls(), max_in_row=max_in_row)

    def __init__(self) -> None:
        self.keyboard = [[]]

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: keyboard={self.keyboard!r}>"

    def copy(self, **with_changes: typing.Any) -> typing.Self:
        new_keyboard = type(self)()
        new_keyboard.keyboard = copy_keyboard(self.keyboard)
        return new_keyboard

    @bound_keyboard_method
    def dict(self) -> DictStrAny:
        return dict(inline_keyboard=[row for row in self.keyboard if row])

    @bound_keyboard_method
    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup.from_dict(self.dict())


__all__ = ("InlineKeyboard", "Keyboard")
