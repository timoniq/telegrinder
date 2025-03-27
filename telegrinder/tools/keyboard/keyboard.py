from __future__ import annotations

import dataclasses
import typing
from copy import deepcopy

from telegrinder.tools.keyboard.base import BaseKeyboard, DictStrAny
from telegrinder.tools.keyboard.data import KeyboardModel
from telegrinder.types.objects import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

if typing.TYPE_CHECKING:
    from telegrinder.tools.keyboard.abc import RawKeyboard


@dataclasses.dataclass(kw_only=True, frozen=True)
class KeyboardModelMixin(KeyboardModel if typing.TYPE_CHECKING else object):
    keyboard_model: KeyboardModel = dataclasses.field(init=False)

    if not typing.TYPE_CHECKING:
        keyboard_model = dataclasses.field(
            default_factory=lambda: KeyboardModel(keyboard=[[]]),
            repr=False,
        )

    @property
    def keyboard(self) -> RawKeyboard:
        return self.keyboard_model.keyboard  # type: ignore
    
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
        return self.keyboard_model.selective

    @property
    def input_field_placeholder(self) -> str | None:
        return self.keyboard_model.input_field_placeholder


@dataclasses.dataclass(frozen=True, kw_only=True)
class Keyboard(KeyboardModelMixin, BaseKeyboard):
    if not typing.TYPE_CHECKING:
        def __init__(self, **kwargs):
            super().__init__(keyboard_model=kwargs.pop("keyboard_model", None) or KeyboardModel(**kwargs))

    def dict(self) -> DictStrAny:
        return dataclasses.asdict(self.keyboard_model) | {"keyboard": [row for row in self.keyboard if row]}

    def get_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup.from_dict(self.dict())

    def copy(self, **with_changes: typing.Any) -> typing.Self:
        return dataclasses.replace(
            self,
            keyboard_model=dataclasses.replace(
                self.keyboard_model,
                keyboard=deepcopy(self.keyboard_model.keyboard),
                **with_changes,
            ),
        )

    def get_keyboard_remove(self) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove.from_data(
            remove_keyboard=True,
            selective=self.keyboard_model.selective,
        )

    def resize(self) -> typing.Self:
        return self.copy(resize_keyboard=True)
    
    def one_time(self) -> typing.Self:
        return self.copy(one_time_keyboard=True)
    
    def selective(self) -> typing.Self:
        return self.copy(selective=True)

    def persistent(self) -> typing.Self:
        return self.copy(is_persistent=True)

    def no_resize(self) -> typing.Self:
        return self.copy(resize_keyboard=False)

    def no_one_time(self) -> typing.Self:
        return self.copy(one_time_keyboard=False)
    
    def no_selective(self) -> typing.Self:
        return self.copy(selective=False)

    def no_persistent(self) -> typing.Self:
        return self.copy(is_persistent=False)

    def placeholder(self, value: str | None, /) -> typing.Self:
        return self.copy(input_field_placeholder=value)


@dataclasses.dataclass(frozen=True)
class InlineKeyboard(BaseKeyboard):
    keyboard: RawKeyboard = dataclasses.field(init=False)

    if not typing.TYPE_CHECKING:
        keyboard = dataclasses.field(
            default_factory=lambda: [[]],
            repr=False,
        )

    def dict(self) -> DictStrAny:
        return dict(inline_keyboard=[row for row in self.keyboard if row])

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup.from_dict(self.dict())

    def copy(self, **_: typing.Any) -> typing.Self:
        return dataclasses.replace(self, keyboard=deepcopy(self.keyboard))


__all__ = ("InlineKeyboard", "Keyboard")
