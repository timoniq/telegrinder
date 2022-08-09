from .abc import ABCMessageRule, Message, patcher
import typing
import vbml

PatternLike = typing.Union[str, vbml.Pattern]


class Markup(ABCMessageRule):
    def __init__(self, patterns: typing.Union[PatternLike, typing.List[PatternLike]]):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, message: Message, ctx: dict) -> bool:
        for pattern in self.patterns:
            response = patcher.check(pattern, message.text)
            if response is False:
                continue
            ctx.update(response)
            return True
        return False
