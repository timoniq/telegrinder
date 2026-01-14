import enum

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.text import Text


class EnumTextRule[T: enum.Enum](ABCRule):
    def __init__(self, enum_t: type[T], *, lower_case: bool = True) -> None:
        self.lower_case = lower_case
        self.enum_t = enum_t
        self.enumerations_map = {
            (enumeration.value.lower() if lower_case else enumeration.value): enumeration for enumeration in self.enum_t
        }

    def find(self, s: str) -> T | None:
        s = s.lower() if self.lower_case else s
        return self.enumerations_map.get(s)

    def check(self, text: Text, ctx: Context) -> bool:
        match self.find(text):
            case enum.Enum() as enumeration:
                ctx.enum_text = enumeration
                return True
            case _:
                return False


__all__ = ("EnumTextRule",)
