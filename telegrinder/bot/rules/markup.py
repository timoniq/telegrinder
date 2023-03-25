from .abc import Message, patcher
from .text import TextMessageRule
import typing
import vbml

PatternLike = str | vbml.Pattern


def check_string(patterns: PatternLike | list[PatternLike], s: str, ctx: dict) -> bool:
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


class Markup(TextMessageRule):
    def __init__(self, patterns: PatternLike | list[PatternLike]):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, message: Message, ctx: dict) -> bool:
        return check_string(self.patterns, message.text, ctx)
