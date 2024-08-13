import re
import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.node.text import Text

from .abc import ABCRule

PatternLike: typing.TypeAlias = str | typing.Pattern[str]


class Regex(ABCRule):
    def __init__(self, regexp: PatternLike | list[PatternLike]) -> None:
        self.regexp: list[re.Pattern[str]] = []
        match regexp:
            case re.Pattern() as pattern:
                self.regexp.append(pattern)
            case str(regex):
                self.regexp.append(re.compile(regex))
            case _:
                self.regexp.extend(
                    re.compile(regexp) if isinstance(regexp, str) else regexp for regexp in regexp
                )

    async def check(self, text: Text, ctx: Context) -> bool:
        for regexp in self.regexp:
            response = re.match(regexp, text)
            if response is not None:
                if matches := response.groupdict():
                    ctx |= matches
                else:
                    ctx |= {"matches": response.groups() or (response.group(),)}
                return True
        return False


__all__ = ("Regex",)
