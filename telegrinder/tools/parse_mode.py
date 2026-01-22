import typing

from telegrinder.tools.final import Final


@typing.final
class ParseMode(Final):
    MARKDOWNV2: typing.Final[typing.Literal["MarkdownV2"]] = "MarkdownV2"
    HTML: typing.Final[typing.Literal["HTML"]] = "HTML"


__all__ = ("ParseMode",)
