from __future__ import annotations

import html
import string
import types
import typing
from contextlib import suppress

from telegrinder.tools.formatting.deep_links import tg_mention_link
from telegrinder.tools.parse_mode import ParseMode
from telegrinder.types.enums import ProgrammingLanguage

type HTMLFormat = str | TagFormat
type Formatter = typing.Callable[[str], TagFormat]

HTML_UNION_SPECIFIERS_SEPARATOR: typing.Final[str] = "+"
TAG_FORMAT: typing.Final[str] = "<{tag}{data}>{content}</{tag}>"
QUOT_MARK: typing.Final[str] = '"'


def escape(string: str, /) -> EscapedString:
    if isinstance(string, EscapedString | HTMLFormatter):
        return EscapedString(string)
    return EscapedString(html.escape(string, quote=False))


def block_quote(string: str, /, *, expandable: bool = False) -> TagFormat:
    return TagFormat(
        string,
        tag="blockquote",
        **{} if not expandable else dict(expandable=None),
    )


def bold(string: str, /) -> TagFormat:
    return TagFormat(string, tag="b")


def code_inline(string: str, /) -> TagFormat:
    return TagFormat(string, tag="code")


def italic(string: str, /) -> TagFormat:
    return TagFormat(string, tag="i")


def link(href: str, /, *, text: str | None = None) -> TagFormat:
    return TagFormat(
        text or href,
        tag="a",
        href=QUOT_MARK + href + QUOT_MARK,
    )


def pre_code(string: str, /, *, lang: str | ProgrammingLanguage | None = None) -> TagFormat:
    if lang is None:
        return TagFormat(string, tag="pre")

    lang = lang.value if isinstance(lang, ProgrammingLanguage) else lang
    return pre_code(TagFormat(string, tag="code", **{"class": f"language-{lang}"}))


def spoiler(string: str, /) -> TagFormat:
    return TagFormat(string, tag="tg-spoiler")


def strike(string: str, /) -> TagFormat:
    return TagFormat(string, tag="s")


def mention(string: str, /, *, user_id: int) -> TagFormat:
    return link(tg_mention_link(user_id=user_id), text=string)


def tg_emoji(string: str, /, *, emoji_id: int) -> TagFormat:
    return TagFormat(string, tag="tg-emoji", emoji_id=emoji_id)


def underline(string: str, /) -> TagFormat:
    return TagFormat(string, tag="u")


class StringFormatterProto(typing.Protocol):
    def format_field(self, value: typing.Any, fmt: str) -> HTMLFormatter: ...

    def format(self, __string: str, *args: object, **kwargs: object) -> HTMLFormatter: ...


class StringFormatter(string.Formatter):
    """String formatter, using substitutions from args and kwargs.
    The substitutions are identified by braces ('{' and '}') with
    specifiers: `bold`, `italic`, `underline`, `strike` etc...
    """

    __formatters__: typing.ClassVar[types.MappingProxyType[str, Formatter]] = types.MappingProxyType(
        mapping={
            "bold": bold,
            "code": code_inline,
            "code_inline": code_inline,
            "italic": italic,
            "spoiler": spoiler,
            "strikethrough": strike,
            "strike": strike,
            "underline": underline,
            "block_quote": block_quote,
            "blockquote": block_quote,
            "expandable_blockquote": lambda string: block_quote(string, expandable=True),
        },
    )

    def validate_html_format(self, value: typing.Any, fmt: str) -> HTMLFormat:
        if not fmt:
            raise ValueError("Formats union should be: format+format.")

        if fmt not in self.__formatters__:
            raise ValueError(
                "Unknown format {!r} for object of type {!r}.".format(
                    fmt,
                    type(value).__name__,
                )
            )

        return fmt

    def make_tag_format(self, value: typing.Any, fmts: list[HTMLFormat]) -> TagFormat:
        formatters = type(self).__formatters__
        current_format = formatters[fmts.pop(0)](
            str(value)
            if isinstance(value, TagFormat)
            else escape(FormatString(value) if not isinstance(value, str) else value)
        )

        for fmt in fmts:
            current_format = formatters[fmt](current_format)

        return (
            TagFormat(
                current_format,
                tag=value.tag,
                **value.data,
            )
            if isinstance(value, TagFormat)
            else current_format
        )

    def format_field(self, value: typing.Any, fmt: str) -> HTMLFormatter:
        with suppress(ValueError):
            return HTMLFormatter(format(value.formatting() if isinstance(value, TagFormat) else value, fmt))

        fmts = list(
            map(
                lambda fmt: self.validate_html_format(value, fmt),
                fmt.split(HTML_UNION_SPECIFIERS_SEPARATOR),
            ),
        )
        return self.make_tag_format(value, fmts).formatting()

    def format(self, __string: str, *args: object, **kwargs: object) -> HTMLFormatter:
        return HTMLFormatter(super().format(__string, *args, **kwargs))


class FormatString(str):
    STRING_FORMATTER: StringFormatterProto = StringFormatter()

    def __new__(cls, string: str = "", /) -> typing.Self:
        if isinstance(string, TagFormat):
            return super().__new__(cls, string.formatting())
        return super().__new__(cls, string)

    def __add__(self, value: str, /) -> HTMLFormatter:
        """Returns self+value."""
        return HTMLFormatter(
            str.__add__(
                escape(self),
                value.formatting() if isinstance(value, TagFormat) else escape(value),
            )
        )

    def __radd__(self, value: str, /) -> HTMLFormatter:
        """Returns value+self."""
        return HTMLFormatter(FormatString.__add__(FormatString(value), self).as_str())

    def __iadd__(self, value: str, /) -> HTMLFormatter:
        """Returns self+=value."""
        return self.__add__(value)

    def as_str(self) -> str:
        """Returns self as a standart string."""
        return self.__str__()

    def format(self, *args: object, **kwargs: object) -> HTMLFormatter:
        return self.STRING_FORMATTER.format(self, *args, **kwargs)

    def join(self, iterable: typing.Iterable[str], /) -> HTMLFormatter:
        html_string = HTMLFormatter()
        max_index = sum(1 for _ in iterable) - 1

        for cur_index, string in enumerate(iterable):
            html_string += string

            if self and cur_index != max_index:
                html_string += self

        return html_string


class EscapedString(FormatString):
    @property
    def former_string(self) -> str:
        return html.unescape(self)


class TagFormat(FormatString):
    tag: str
    data: dict[str, typing.Any]

    def __new__(
        cls,
        string: str,
        /,
        *,
        tag: str,
        **data: typing.Any | None,
    ) -> typing.Self:
        if isinstance(string, TagFormat):
            string = string.formatting()
        elif not isinstance(
            string,
            (
                EscapedString,
                HTMLFormatter,
            ),
        ):
            string = escape(string)

        obj = super().__new__(cls, string)
        obj.tag = tag
        obj.data = data
        return obj

    def get_tag_data(self) -> str:
        return "".join(f" {k}={v}" if v is not None else f" {k}" for k, v in self.data.items())

    def formatting(self) -> HTMLFormatter:
        return HTMLFormatter(
            TAG_FORMAT.format(
                tag=self.tag,
                data=self.get_tag_data(),
                content=self,
            )
        )


class HTMLFormatter(FormatString):
    """>>> HTMLFormatter(bold("Hello, World"))
    '<b>Hello, World</b>'
    >>> HTMLFormatter("Hi, {name:italic}").format(name="Max")
    'Hi, <i>Max</i>'
    """

    PARSE_MODE: typing.Final[str] = ParseMode.HTML


__all__ = (
    "FormatString",
    "HTMLFormatter",
    "block_quote",
    "bold",
    "code_inline",
    "escape",
    "italic",
    "link",
    "mention",
    "pre_code",
    "spoiler",
    "strike",
    "tg_emoji",
    "underline",
)
