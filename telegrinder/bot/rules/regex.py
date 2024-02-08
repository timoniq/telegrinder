import re
import typing

from telegrinder.bot.dispatch.context import Context

from .abc import Message
from .text import TextMessageRule

PatternLike = str | typing.Pattern[str]


class Regex(TextMessageRule):
    def __init__(self, regexp: PatternLike | list[PatternLike]):
        self.regexp: list[re.Pattern[str]] = []
        match regexp:
            case re.Pattern() as pattern:
                self.regexp.append(pattern)
            case str(regex):
                self.regexp.append(re.compile(regex))
            case _:
                self.regexp.extend(
                    re.compile(regexp) if isinstance(regexp, str) else regexp
                    for regexp in regexp
                )

    async def check(self, message: Message, ctx: Context) -> bool:
        for regexp in self.regexp:
            response = re.match(regexp, message.text.unwrap())
            if response is not None:
                if matches := response.groupdict():
                    ctx |= matches
                else:
                    ctx |= {"matches": response.groups() or (response.group(),)}
                return True
        return False


__all__ = ("Regex",)
