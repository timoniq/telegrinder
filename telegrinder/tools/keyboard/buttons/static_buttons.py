import dataclasses
import types
import typing
from functools import cached_property

from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.payload import PayloadJsonEqRule, PayloadMarkupRule, PayloadModelRule
from telegrinder.bot.rules.text import Text
from telegrinder.node.base import Node
from telegrinder.node.payload import PayloadData
from telegrinder.tools.keyboard.buttons.base import BaseStaticButton
from telegrinder.tools.keyboard.buttons.buttons import Button, CallbackData, InlineButton


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
    callback_data_type: type[CallbackData | None]

    if not typing.TYPE_CHECKING:

        def __init__(self, *args, **kwargs):
            self.row = kwargs.pop("row", False)
            InlineButton.__init__(self, *args, **kwargs)

        check = lambda self, *args, **kwargs: False
    else:

        def check(self, *args: typing.Any, **kwargs: typing.Any) -> bool: ...

    def __post_init__(self) -> None:
        self.callback_data_type = type(self.callback_data)

        if isinstance(self.callback_data, str):
            self.check = PayloadMarkupRule(self.callback_data).check
        elif isinstance(self.callback_data, dict):
            self.check = PayloadJsonEqRule(self.callback_data).check
        elif not isinstance(self.callback_data, (bytes, types.NoneType)):
            self.check = PayloadModelRule(
                type(self.callback_data),
                serializer=type(self.callback_data_serializer) if self.callback_data_serializer else None,
            ).check

        super().__post_init__()

    @cached_property
    def required_nodes(self) -> dict[str, type[Node]]:
        return {"payload": PayloadData[self.callback_data_type, type(self.callback_data_serializer)]}  # type: ignore


__all__ = ("StaticButton", "StaticInlineButton")
