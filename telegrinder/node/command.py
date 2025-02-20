import typing
from dataclasses import dataclass, field

from fntypes.option import Nothing, Option, Some

from telegrinder.node.base import DataNode
from telegrinder.node.either import Either
from telegrinder.node.text import Caption, Text


def single_split(s: str, separator: str) -> tuple[str, str]:
    left, *right = s.split(separator, 1)
    return left, (right[0] if right else "")


def cut_mention(text: str) -> tuple[str, Option[str]]:
    left, right = single_split(text, "@")
    return left, Some(right) if right else Nothing()


@dataclass(slots=True)
class CommandInfo(DataNode):
    name: str
    arguments: str
    mention: Option[str] = field(default_factory=Nothing)

    @classmethod
    def compose(cls, text: Either[Text, Caption]) -> typing.Self:
        name, arguments = single_split(text, separator=" ")
        name, mention = cut_mention(name)
        return cls(name, arguments, mention)


__all__ = ("CommandInfo", "cut_mention", "single_split")
