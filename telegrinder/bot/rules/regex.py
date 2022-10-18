import re
import typing

from .abc import Message
from .text import ABCTextMessageRule

PatternLike = typing.Union[str, typing.Pattern]


class Regex(ABCTextMessageRule):
    def __init__(self, regexp: typing.Union[PatternLike, typing.List[PatternLike]]):
        if isinstance(regexp, re.Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        else:
            regexp = [
                re.compile(regexp) if isinstance(regexp, str) else regexp
                for regexp in regexp
            ]

        self.regexp = regexp

    async def check(self, message: Message, ctx: dict) -> bool:
        for regexp in self.regexp:
            match = re.match(regexp, message.text)
            if match:
                ctx.update({"match": match.groups()})
                return True
        return False
