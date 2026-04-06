import abc
import dataclasses
import typing
from functools import cached_property

import msgspec

from telegrinder.msgspec_utils.encoder import encoder
from telegrinder.tools.keyboard.utils import freaky_keyboard_merge
from telegrinder.tools.serialization.json_ser import JSONSerializer
from telegrinder.tools.serialization.utils import get_model_serializer
from telegrinder.types.objects import (
    CallbackGame,
    CopyTextButton,
    KeyboardButtonPollType,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    KeyboardButtonStyle,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance

    from telegrinder.bot.rules.abc import ABCRule
    from telegrinder.bot.rules.button import ButtonRule
    from telegrinder.tools.keyboard import keyboard
    from telegrinder.tools.keyboard.base import BaseKeyboard
    from telegrinder.tools.keyboard.button import BaseButton
    from telegrinder.tools.serialization.abc import ABCDataSerializer

type CallbackData = str | dict[str, typing.Any] | DataclassInstance | msgspec.Struct
type Keyboard = keyboard.Keyboard
type InlineKeyboard = keyboard.InlineKeyboard


@dataclasses.dataclass(kw_only=True)
class BaseButton[T: BaseKeyboard = typing.Any](abc.ABC):
    new_row: bool = dataclasses.field(default=False, repr=False)
    style: KeyboardButtonStyle | None = dataclasses.field(default=None)
    icon_id: dataclasses.InitVar[str | int | None] = dataclasses.field(default=None)
    icon_custom_emoji_id: str | None = dataclasses.field(default=None, init=False)

    def __post_init__(self, icon_id: str | int | None) -> None:
        if icon_id is not None:
            self.icon_custom_emoji_id = icon_id if isinstance(icon_id, str) else str(icon_id)

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
class BaseDangerButton[T: BaseKeyboard = typing.Any](BaseButton[T]):
    style: KeyboardButtonStyle = dataclasses.field(default=KeyboardButtonStyle.DANGER, init=False)


@dataclasses.dataclass
class BaseSuccessButton[T: BaseKeyboard = typing.Any](BaseButton[T]):
    style: KeyboardButtonStyle = dataclasses.field(default=KeyboardButtonStyle.SUCCESS, init=False)


@dataclasses.dataclass
class BasePrimaryButton[T: BaseKeyboard = typing.Any](BaseButton[T]):
    style: KeyboardButtonStyle = dataclasses.field(default=KeyboardButtonStyle.PRIMARY, init=False)


@dataclasses.dataclass
class Button(BaseButton[Keyboard]):
    text: str
    request_contact: bool | None = dataclasses.field(default=None, kw_only=True)
    request_location: bool | None = dataclasses.field(default=None, kw_only=True)
    request_chat: KeyboardButtonRequestChat | None = dataclasses.field(
        default=None,
        kw_only=True,
    )
    request_users: KeyboardButtonRequestUsers | None = dataclasses.field(default=None, kw_only=True)
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
class DangerButton(BaseDangerButton[Keyboard], Button):
    """Red button."""


@dataclasses.dataclass
class SuccessButton(BaseSuccessButton[Keyboard], Button):
    """Green button."""


@dataclasses.dataclass
class PrimaryButton(BasePrimaryButton[Keyboard], Button):
    """Blue button."""


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

    def __post_init__(self, icon_id: str | int | None) -> None:
        super().__post_init__(icon_id)

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


@dataclasses.dataclass
class DangerInlineButton(BaseDangerButton[InlineKeyboard], InlineButton):
    """Red inline button."""


@dataclasses.dataclass
class SuccessInlineButton(BaseSuccessButton[InlineKeyboard], InlineButton):
    """Green inline button."""


@dataclasses.dataclass
class PrimaryInlineButton(BasePrimaryButton[InlineKeyboard], InlineButton):
    """Blue inline button."""


__all__ = (
    "BaseButton",
    "Button",
    "DangerButton",
    "DangerInlineButton",
    "InlineButton",
    "PrimaryButton",
    "PrimaryInlineButton",
    "SuccessButton",
    "SuccessInlineButton",
)
