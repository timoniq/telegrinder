from __future__ import annotations

import dataclasses
import types
import typing

import msgspec

from telegrinder.msgspec_utils import encoder
from telegrinder.tools.callback_data_serilization import ABCDataSerializer, JSONSerializer
from telegrinder.tools.keyboard.buttons.base import BaseButton
from telegrinder.types.objects import (
    CallbackGame,
    CopyTextButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

    from telegrinder.tools.keyboard.abc import ABCKeyboard
    from telegrinder.tools.keyboard.keyboard import InlineKeyboard, Keyboard

type CallbackData = str | bytes | dict[str, typing.Any] | DataclassInstance | msgspec.Struct


def _magic_add_buttons(
    name_keyboard: str,
    button: BaseButton,
    other_button: typing.Any,
    /,
    *,
    row: bool = False,
) -> ABCKeyboard | types.NotImplementedType:
    if not isinstance(other_button, type(button)):
        return NotImplemented

    from telegrinder.tools.keyboard.keyboard import InlineKeyboard, Keyboard  # noqa

    keyboard = locals()[name_keyboard]().add(button)
    if row:
        keyboard = keyboard.row()
    return keyboard.add(other_button)


@dataclasses.dataclass
class Button(BaseButton):
    text: str
    request_contact: bool = dataclasses.field(default=False, kw_only=True)
    request_location: bool = dataclasses.field(default=False, kw_only=True)
    request_chat: KeyboardButtonRequestChat | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    request_user: KeyboardButtonRequestUsers | None = dataclasses.field(default=None, kw_only=True)
    request_poll: KeyboardButtonPollType | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    web_app: WebAppInfo | None = dataclasses.field(default=None, kw_only=True)

    def __or__(self, other: object, /) -> Keyboard:
        return _magic_add_buttons("Keyboard", self, other)

    def __matmul__(self, other: object, /) -> Keyboard:
        return _magic_add_buttons("Keyboard", self, other, row=True)


@dataclasses.dataclass
class InlineButton(BaseButton):
    text: str
    url: str | None = dataclasses.field(default=None, kw_only=True)
    login_url: LoginUrl | None = dataclasses.field(default=None, kw_only=True)
    pay: bool | None = dataclasses.field(default=None, kw_only=True)
    callback_data: CallbackData | None = dataclasses.field(default=None, kw_only=True)
    callback_data_serializer: dataclasses.InitVar[ABCDataSerializer[typing.Any] | None] = dataclasses.field(
        default=None,
        kw_only=True,
    )
    callback_game: CallbackGame | None = dataclasses.field(default=None, kw_only=True)
    copy_text: str | CopyTextButton | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_current_chat: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    web_app: str | WebAppInfo | None = dataclasses.field(default=None, kw_only=True)

    def __post_init__(self, callback_data_serializer: ABCDataSerializer[typing.Any] | None) -> None:
        if (
            callback_data_serializer is None
            and isinstance(self.callback_data, msgspec.Struct | dict)
            or dataclasses.is_dataclass(self.callback_data)
        ):
            callback_data_serializer = callback_data_serializer or JSONSerializer(
                type(self.callback_data),
            )

        if callback_data_serializer is not None:
            self.callback_data = callback_data_serializer.serialize(self.callback_data)
        elif self.callback_data is not None and not isinstance(self.callback_data, str | bytes):
            self.callback_data = encoder.encode(self.callback_data)

        if isinstance(self.copy_text, str):
            self.copy_text = CopyTextButton(text=self.copy_text)

        if isinstance(self.web_app, str):
            self.web_app = WebAppInfo(url=self.web_app)

    def __or__(self, other: object, /) -> InlineKeyboard:
        return _magic_add_buttons("InlineKeyboard", self, other)

    def __matmul__(self, other: object, /) -> InlineKeyboard:
        return _magic_add_buttons("InlineKeyboard", self, other, row=True)


__all__ = ("Button", "InlineButton")
