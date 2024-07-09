import dataclasses
import typing

import msgspec

from telegrinder.model import encoder
from telegrinder.types import (
    CallbackGame,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)
from telegrinder.types.objects import LoginUrl

ButtonT = typing.TypeVar("ButtonT", bound="BaseButton")


@typing.runtime_checkable
class DataclassInstance(typing.Protocol):
    __dataclass_fields__: typing.ClassVar[dict[str, dataclasses.Field[typing.Any]]]


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


@dataclasses.dataclass
class Button(BaseButton):
    text: str
    _: dataclasses.KW_ONLY
    request_contact: bool = False
    request_location: bool = False
    request_chat: dict[str, typing.Any] | KeyboardButtonRequestChat | None = None
    request_user: dict[str, typing.Any] | KeyboardButtonRequestUsers | None = None
    request_poll: dict[str, typing.Any] | KeyboardButtonPollType | None = None
    web_app: dict[str, typing.Any] | WebAppInfo | None = None


@dataclasses.dataclass
class InlineButton(BaseButton):
    text: str
    _: dataclasses.KW_ONLY
    url: str | None = None
    login_url: dict[str, typing.Any] | LoginUrl | None = None
    pay: bool | None = None
    callback_data: str | dict[str, typing.Any] | DataclassInstance | msgspec.Struct | None = None
    callback_game: dict[str, typing.Any] | CallbackGame | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    switch_inline_query_chosen_chat: dict[str, typing.Any] | SwitchInlineQueryChosenChat | None = None
    web_app: dict[str, typing.Any] | WebAppInfo | None = None


__all__ = (
    "BaseButton",
    "Button",
    "DataclassInstance",
    "InlineButton",
    "RowButtons",
)
