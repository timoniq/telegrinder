from __future__ import annotations

import dataclasses
import typing

import msgspec

from telegrinder.types.objects import (
    CallbackGame,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

from .callback_data_serilization import ABCDataSerializer, JSONSerializer, MsgPackSerializer

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

KeyboardButton = typing.TypeVar("KeyboardButton", bound="BaseButton")

CallbackData: typing.TypeAlias = (
    "str | bytes | dict[str, typing.Any] | DataclassInstance | msgspec.Struct | ABCDataSerializer[typing.Any]"
)


@dataclasses.dataclass
class BaseButton:
    def get_data(self) -> dict[str, typing.Any]:
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


class RowButtons(typing.Generic[KeyboardButton]):
    buttons: list[KeyboardButton]
    auto_row: bool

    def __init__(self, *buttons: KeyboardButton, auto_row: bool = True) -> None:
        self.buttons = list(buttons)
        self.auto_row = auto_row

    def get_data(self) -> list[dict[str, typing.Any]]:
        return [b.get_data() for b in self.buttons]


@dataclasses.dataclass
class Button(BaseButton):
    text: str
    request_contact: bool = dataclasses.field(default=False, kw_only=True)
    request_location: bool = dataclasses.field(default=False, kw_only=True)
    request_chat: dict[str, typing.Any] | KeyboardButtonRequestChat | None = dataclasses.field(
        default=None, kw_only=True
    )
    request_user: dict[str, typing.Any] | KeyboardButtonRequestUsers | None = dataclasses.field(
        default=None, kw_only=True
    )
    request_poll: dict[str, typing.Any] | KeyboardButtonPollType | None = dataclasses.field(
        default=None, kw_only=True
    )
    web_app: dict[str, typing.Any] | WebAppInfo | None = dataclasses.field(default=None, kw_only=True)


@dataclasses.dataclass
class InlineButton(BaseButton):
    text: str
    url: str | None = dataclasses.field(default=None, kw_only=True)
    login_url: dict[str, typing.Any] | LoginUrl | None = dataclasses.field(default=None, kw_only=True)
    pay: bool | None = dataclasses.field(default=None, kw_only=True)
    callback_data: CallbackData | None = dataclasses.field(default=None, kw_only=True)
    callback_game: dict[str, typing.Any] | CallbackGame | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_current_chat: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_chosen_chat: dict[str, typing.Any] | SwitchInlineQueryChosenChat | None = (
        dataclasses.field(default=None, kw_only=True)
    )
    web_app: dict[str, typing.Any] | WebAppInfo | None = dataclasses.field(default=None, kw_only=True)

    @staticmethod
    def compose_callback_data(callback_data: CallbackData) -> str | bytes:
        if isinstance(callback_data, dict):
            return JSONSerializer.serialize_from_json(callback_data)
        if isinstance(callback_data, msgspec.Struct) or dataclasses.is_dataclass(callback_data):
            return MsgPackSerializer.serialize_from_model(callback_data)
        if isinstance(callback_data, ABCDataSerializer):
            return callback_data.serialize(callback_data)
        return callback_data

    def get_data(self) -> dict[str, typing.Any]:
        if self.callback_data is not None:
            self.callback_data = self.compose_callback_data(self.callback_data)
        return super().get_data()


__all__ = (
    "BaseButton",
    "Button",
    "InlineButton",
    "RowButtons",
)
