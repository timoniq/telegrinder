import dataclasses
import typing

import msgspec

from telegrinder.msgspec_utils import encoder
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

from .callback_data_serilization import ABCDataSerializer, JSONSerializer

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

type CallbackData = str | bytes | dict[str, typing.Any] | DataclassInstance | msgspec.Struct


@dataclasses.dataclass
class BaseButton:
    def get_data(self) -> dict[str, typing.Any]:
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


class RowButtons[KeyboardButton: BaseButton]:
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
                self.callback_data.__class__,
            )

        if callback_data_serializer is not None:
            self.callback_data = callback_data_serializer.serialize(self.callback_data)
        elif not isinstance(self.callback_data, str | bytes):
            self.callback_data = encoder.encode(self.callback_data)

        if isinstance(self.copy_text, str):
            self.copy_text = CopyTextButton(text=self.copy_text)

        if isinstance(self.web_app, str):
            self.web_app = WebAppInfo(url=self.web_app)


__all__ = (
    "BaseButton",
    "Button",
    "InlineButton",
    "RowButtons",
)
