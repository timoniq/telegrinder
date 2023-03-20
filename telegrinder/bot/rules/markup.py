from .abc import Message
from .text import ABCTextMessageRule
import typing
import vbml

PatternLike = typing.Union[str, vbml.Pattern]


def check_string(
    patterns: typing.Union[PatternLike, typing.List[PatternLike]], s: str, ctx: dict,
    patcher: vbml.Patcher
) -> bool:
    if s is None:
        return False
    for pattern in patterns:
        response = patcher.check(pattern, s)
        if response in (False, None):
            continue
        elif isinstance(response, dict):
            ctx.update(response)
        return True
    return False


class Markup(ABCTextMessageRule):
    def __init__(self, patterns: typing.Union[PatternLike, typing.List[PatternLike]]):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, message: Message, ctx: dict, patcher: vbml.Patcher) -> bool:
        return check_string(self.patterns, message.text, ctx, patcher)
