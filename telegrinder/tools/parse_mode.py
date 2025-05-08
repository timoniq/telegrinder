import typing

from telegrinder.tools.final import Final


@typing.final
class ParseMode(Final):
    MARKDOWNV2: typing.Final[str] = "MarkdownV2"
    HTML: typing.Final[str] = "HTML"


__all__ = ("ParseMode",)
