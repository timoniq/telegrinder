from __future__ import annotations

import abc
import dataclasses
import typing
from functools import cached_property

import msgspec

from telegrinder.msgspec_utils.encoder import encoder
from telegrinder.tools.callback_data_serialization.json_ser import JSONSerializer
from telegrinder.tools.callback_data_serialization.utils import get_model_serializer
from telegrinder.tools.keyboard.utils import freaky_keyboard_merge
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

    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.bot.rules.button import ButtonRule
    from telegrinder.tools.callback_data_serialization.abc import ABCDataSerializer
    from telegrinder.tools.keyboard import keyboard
    from telegrinder.tools.keyboard.base import BaseKeyboard
    from telegrinder.tools.keyboard.button import BaseButton

type CallbackData = str | dict[str, typing.Any] | DataclassInstance | msgspec.Struct
type Keyboard = keyboard.Keyboard
type InlineKeyboard = keyboard.InlineKeyboard


@dataclasses.dataclass(kw_only=True)
class BaseButton[T: BaseKeyboard = typing.Any](abc.ABC):
    new_row: bool = dataclasses.field(default=False)

    @property
    @abc.abstractmethod
    def keyboard_class(self) -> type[T]:
        pass

    @property
    @abc.abstractmethod
    def rule(self) -> ABCRule:
        pass

    if typing.TYPE_CHECKING:

        def __get__(self, instance: T | None, owner: type[T]) -> ButtonRule[typing.Self]: ...

        @property
        def as_keyboard(self: BaseButton[T]) -> type[T]: ...
    else:

        def as_keyboard(self, *args, **kwargs):
            return self.keyboard_class(*args, **kwargs).add(self)

    def __and__(self, other: object, /) -> T:
        if not isinstance(other, self.keyboard_class | type(self)):
            return NotImplemented
        return freaky_keyboard_merge(self, other)

    def __or__(self, other: object, /) -> T:
        if not isinstance(other, self.keyboard_class | type(self)):
            return NotImplemented
        return freaky_keyboard_merge(self, other, row=True)

    def get_data(self) -> dict[str, typing.Any]:
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None and k != "new_row"}


@dataclasses.dataclass
class Button(BaseButton[Keyboard]):
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

    @cached_property
    def rule(self) -> ABCRule:
        from telegrinder.bot.rules.text import Text

        return Text(self.text)

    @cached_property
    def keyboard_class(self) -> type[Keyboard]:
        from telegrinder.tools.keyboard.keyboard import Keyboard

        return Keyboard


@dataclasses.dataclass
class InlineButton(BaseButton[InlineKeyboard]):
    text: str
    url: str | None = dataclasses.field(default=None, kw_only=True)
    login_url: LoginUrl | None = dataclasses.field(default=None, kw_only=True)
    pay: bool | None = dataclasses.field(default=None, kw_only=True)
    callback_data: CallbackData | None = dataclasses.field(default=None, kw_only=True)
    callback_data_serializer: ABCDataSerializer[typing.Any] | None = dataclasses.field(
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

    def __post_init__(self) -> None:
        model_serializer = get_model_serializer(self.callback_data)

        self.input_callback_data = self.callback_data
        self.callback_data_serializer = self.callback_data_serializer or (
            None if model_serializer is None else model_serializer(type(self.callback_data))
        )

        if (
            self.callback_data_serializer is None
            and isinstance(self.callback_data, msgspec.Struct | dict)
            or dataclasses.is_dataclass(self.callback_data)
        ):
            self.callback_data_serializer = self.callback_data_serializer or JSONSerializer(
                type(self.callback_data),
            )

        if self.callback_data_serializer is not None:
            self.callback_data = self.callback_data_serializer.serialize(self.callback_data)
        elif self.callback_data is not None and not isinstance(self.callback_data, str):
            self.callback_data = encoder.encode(self.callback_data)

        if isinstance(self.copy_text, str):
            self.copy_text = CopyTextButton(text=self.copy_text)

        if isinstance(self.web_app, str):
            self.web_app = WebAppInfo(url=self.web_app)

    @cached_property
    def rule(self) -> ABCRule:
        from telegrinder.bot.rules.payload import PayloadEqRule, PayloadJsonEqRule, PayloadModelRule

        if isinstance(self.input_callback_data, str):
            return PayloadEqRule(self.input_callback_data)

        if isinstance(self.input_callback_data, dict):
            return PayloadJsonEqRule(self.input_callback_data)

        if self.input_callback_data is not None:
            return PayloadModelRule(
                type(self.input_callback_data),
                payload=self.input_callback_data,
                serializer=type(self.callback_data_serializer) if self.callback_data_serializer else None,
            )

        raise ValueError("Cannot create rule, because callback data is not defined.")

    @cached_property
    def keyboard_class(self) -> type[InlineKeyboard]:
        from telegrinder.tools.keyboard.keyboard import InlineKeyboard

        return InlineKeyboard


__all__ = ("BaseButton", "Button", "InlineButton")
