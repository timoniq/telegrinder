import typing


@typing.final
class ParseMode:
    MARKDOWNV2: typing.Final[str] = "MarkdownV2"
    HTML: typing.Final[str] = "HTML"


__all__ = ("ParseMode",)
