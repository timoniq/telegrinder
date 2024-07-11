import enum
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.text import Text

from .abc import ABCRule

T = typing.TypeVar("T", bound=enum.Enum)


class EnumTextRule(ABCRule, typing.Generic[T]):
    def __init__(self, enum_t: type[T], *, lower_case: bool = True) -> None:
        self.enum_t = enum_t
        self.texts = list(
            map(
                lambda x: x.value.lower() if lower_case else x.value,
                self.enum_t,
            )
        )

    def find(self, s: str) -> T:
        for enumeration in self.enum_t:
            if enumeration.value.lower() == s:
                return enumeration
        raise KeyError("Enumeration is undefined.")

    async def check(self, text: Text, ctx: Context) -> bool:
        text = text.lower()  # type: ignore
        if text not in self.texts:
            return False
        ctx.enum_text = self.find(text)
        return True
