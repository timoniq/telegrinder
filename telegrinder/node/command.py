from dataclasses import dataclass, field

from fntypes import Nothing, Option, Some

from .base import DataNode
from .text import Text


def single_split(s: str, separator: str) -> tuple[str, str]:
    left, *right = s.split(separator, 1)
    return left, (right[0] if right else "")


def cut_mention(text: str) -> tuple[str, Option[str]]:
    left, right = single_split(text, '@')
    return left, Some(right) if right else Nothing()


@dataclass
class CommandNode(DataNode):
    name: str
    arguments: str
    mention: Option[str] = field(default_factory=Nothing)

    @classmethod
    async def compose(cls, text: Text):
        name, arguments = single_split(text, separator=" ")  # we suppose name of command and its args are separated by space
        name, mention = cut_mention(name)
        return cls(name, arguments, mention)




