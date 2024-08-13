import dataclasses
import typing

import msgspec

from telegrinder.msgspec_utils import DataclassInstance, encoder
from telegrinder.types.objects import (
    CallbackGame,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

ButtonT = typing.TypeVar("ButtonT", bound="BaseButton")


@dataclasses.dataclass
class BaseButton:
    def get_data(self) -> dict[str, typing.Any]:
        return {
            k: v if k != "callback_data" or isinstance(v, str) else encoder.encode(v)
            for k, v in dataclasses.asdict(self).items()
            if v is not None
        }


class RowButtons(typing.Generic[ButtonT]):
    buttons: list[ButtonT]
    auto_row: bool

    def __init__(self, *buttons: ButtonT, auto_row: bool = True) -> None:
        self.buttons = list(buttons)
        self.auto_row = auto_row

    def get_data(self) -> list[dict[str, typing.Any]]:
        return [b.get_data() for b in self.buttons]


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass(slots=True)
class InlineButton(BaseButton):
    text: str
    url: str | None = dataclasses.field(default=None, kw_only=True)
    login_url: dict[str, typing.Any] | LoginUrl | None = dataclasses.field(default=None, kw_only=True)
    pay: bool | None = dataclasses.field(default=None, kw_only=True)
    callback_data: str | dict[str, typing.Any] | DataclassInstance | msgspec.Struct | None = (
        dataclasses.field(default=None, kw_only=True)
    )
    callback_game: dict[str, typing.Any] | CallbackGame | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_current_chat: str | None = dataclasses.field(default=None, kw_only=True)
    switch_inline_query_chosen_chat: dict[str, typing.Any] | SwitchInlineQueryChosenChat | None = (
        dataclasses.field(default=None, kw_only=True)
    )
    web_app: dict[str, typing.Any] | WebAppInfo | None = dataclasses.field(default=None, kw_only=True)


__all__ = (
    "BaseButton",
    "Button",
    "DataclassInstance",
    "InlineButton",
    "RowButtons",
)
