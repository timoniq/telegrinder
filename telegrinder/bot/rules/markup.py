import re
import typing

import vbml

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.node.either import Either
from telegrinder.node.text import Caption, Text
from telegrinder.tools.global_context.builtin_context import TelegrinderContext

type PatternLike = str | vbml.Pattern

TELEGRINDER_CONTEXT: typing.Final[TelegrinderContext] = TelegrinderContext()


def check_string(patterns: list[vbml.Pattern], s: str, ctx: Context) -> bool:
    for pattern in patterns:
        match TELEGRINDER_CONTEXT.vbml_patcher.check(pattern, s):
            case {**response}:
                ctx |= response
            case None | False:
                continue

        return True

    return False


class Markup(ABCRule):
    """Markup Language. See the [vbml documentation](https://github.com/tesseradecade/vbml/blob/master/docs/index.md)."""

    def __init__(
        self,
        patterns: PatternLike | list[PatternLike],
        /,
        *,
        flags: re.RegexFlag | None = None,
    ) -> None:
        self.patterns = [
            vbml.Pattern(text=pattern, flags=flags or TELEGRINDER_CONTEXT.vbml_pattern_flags)
            if isinstance(pattern, str)
            else pattern
            for pattern in ([patterns] if not isinstance(patterns, list) else patterns)
        ]

    def check(self, text: Either[Text, Caption], ctx: Context) -> bool:
        return check_string(self.patterns, text, ctx)


__all__ = ("Markup", "check_string")
