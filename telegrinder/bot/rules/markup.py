from .abc import Message, patcher
from .text import TextMessageRule
import vbml

PatternLike = str | vbml.Pattern


def check_string(patterns: list[PatternLike], s: str, ctx: dict) -> bool:
    for pattern in patterns:
        match patcher.check(pattern, s):
            case None | False:
                continue
            case {**response}:
                ctx |= response
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
