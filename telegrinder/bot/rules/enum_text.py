import typing
from enum import Enum

from .abc import Message
from .text import TextMessageRule

T = typing.TypeVar("T", bound=Enum, covariant=True)


class EnumTextRule(TextMessageRule, typing.Generic[T]):
    def __init__(self, enum_t: type[T]) -> None:
        self.enum_t = enum_t

    @property
    def texts(self) -> list[str]:
        return list(map(lambda x: x.value.lower(), self.enum_t))

    def find(self, s: str) -> T:
        for enumeration in self.enum_t:
            if enumeration.value.lower() == s:
                return enumeration
        raise KeyError("Enumeration is undefined")

    async def check(self, message: Message, ctx: dict) -> bool:
        text = message.text.unwrap().lower()
        if text not in self.texts:
            return False
        ctx["enum"] = self.find(text)
        return True
