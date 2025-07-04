import dataclasses
import types
import typing

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.payload import PayloadJsonEqRule, PayloadMarkupRule, PayloadModelRule
from telegrinder.bot.rules.text import Text
from telegrinder.tools.callback_data_serialization import ABCDataSerializer
from telegrinder.tools.keyboard.buttons.base import BaseStaticButton
from telegrinder.tools.keyboard.buttons.buttons import Button, InlineButton


@dataclasses.dataclass
class StaticButtonMixin(BaseStaticButton):
    __and__: typing.ClassVar[None] = None
    __or__: typing.ClassVar[None] = None


@dataclasses.dataclass
class StaticButton(StaticButtonMixin, Button, Text):
    if not typing.TYPE_CHECKING:

        def __init__(self, text, **kwargs):
            self.row = kwargs.pop("row", False)
            Button.__init__(self, text=text, **kwargs)
            Text.__init__(self, text)


@dataclasses.dataclass
class StaticInlineButton(StaticButtonMixin, InlineButton, ABCRule):
    if not typing.TYPE_CHECKING:

        def __init__(self, *args, **kwargs):
            self.row = kwargs.pop("row", False)
            InlineButton.__init__(self, *args, **kwargs)

        check = lambda self, *args, **kwargs: False
    else:

        def check(self, *args: typing.Any, **kwargs: typing.Any) -> bool: ...

    def __post_init__(self, callback_data_serializer: ABCDataSerializer[typing.Any] | None) -> None:
        if isinstance(self.callback_data, str):
            self.check = PayloadMarkupRule(self.callback_data).check
        elif isinstance(self.callback_data, dict):
            self.check = PayloadJsonEqRule(self.callback_data).check
        elif not isinstance(self.callback_data, (bytes, types.NoneType)):
            self.check = PayloadModelRule(
                type(self.callback_data),
                serializer=type(callback_data_serializer) if callback_data_serializer else None,
            ).check

        super().__post_init__(callback_data_serializer)


__all__ = ("StaticButton", "StaticInlineButton")
