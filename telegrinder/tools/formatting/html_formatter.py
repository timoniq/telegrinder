from __future__ import annotations

import dataclasses
import html
import string
import typing
from contextlib import suppress

from telegrinder.tools.parse_mode import ParseMode
from telegrinder.types.enums import ProgrammingLanguage

from .deep_links import tg_mention_link
from .spec_html_formats import SpecialFormat, is_spec_format

type HTMLFormat = str | TagFormat

HTML_UNION_SPECIFIERS_SEPARATOR: typing.Final[str] = "+"
TAG_FORMAT: typing.Final[str] = "<{tag}{data}>{content}</{tag}>"
QUOT_MARK: typing.Final[str] = '"'


class StringFormatterProto(typing.Protocol):
    def format_field(self, value: typing.Any, fmt: str) -> HTMLFormatter: ...

    def format(self, __string: str, *args: object, **kwargs: object) -> HTMLFormatter: ...


class StringFormatter(string.Formatter):
    """String formatter, using substitutions from args and kwargs.
    The substitutions are identified by braces ('{' and '}') with
    specifiers: `bold`, `italic`, `underline`, `strike` etc...
    """

    __formats__: typing.ClassVar[tuple[str, ...]] = (
        "bold",
        "code_inline",
        "italic",
        "spoiler",
        "strike",
        "underline",
    )

    def validate_html_format(self, value: typing.Any, fmt: str) -> HTMLFormat:
        if not fmt:
            raise ValueError("Formats union should be: format+format.")

        if fmt not in self.__formats__:
            raise ValueError(
                "Unknown format {!r} for object of type {!r}.".format(
                    fmt,
                    type(value).__name__,
                )
            )

        return fmt

    def get_spec_formatter(self, value: SpecialFormat) -> typing.Callable[..., TagFormat]:
        return globals()[value.__formatter_name__]

    def make_tag_format(self, value: typing.Any, fmts: list[HTMLFormat]) -> TagFormat:
        if is_spec_format(value):
            value = value.string

        current_format = globals()[fmts.pop(0)](
            str(value)
            if isinstance(value, TagFormat)
            else escape(FormatString(value) if not isinstance(value, str) else value)
        )
        for fmt in fmts:
            current_format = globals()[fmt](current_format)

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
            return HTMLFormatter(
                format(
                    (
                        value.formatting()
                        if isinstance(value, TagFormat)
                        else (
                            self.get_spec_formatter(value)(**dataclasses.asdict(value)).formatting()
                            if is_spec_format(value)
                            else value
                        )
                    ),
                    fmt,
                )
            )

        fmts = list(
            map(
                lambda fmt: self.validate_html_format(value, fmt),
                fmt.split(HTML_UNION_SPECIFIERS_SEPARATOR),
            ),
        )
        tag_format = self.make_tag_format(value, fmts)

        if is_spec_format(value):
            value.string = tag_format
            tag_format = self.get_spec_formatter(value)(**dataclasses.asdict(value))

        return tag_format.formatting()

    def format(self, __string: str, *args: object, **kwargs: object) -> HTMLFormatter:
        return HTMLFormatter(super().format(__string, *args, **kwargs))


class FormatString(str):
    STRING_FORMATTER: StringFormatterProto = StringFormatter()

    def __new__(cls, string: str, /) -> typing.Self:
        if isinstance(string, TagFormat):
            return super().__new__(cls, string.formatting())
        return super().__new__(cls, string)

    def __add__(self, value: str) -> HTMLFormatter:
        """Returns self+value."""
        return HTMLFormatter(
            str.__add__(
                escape(self),
                value.formatting() if isinstance(value, TagFormat) else escape(value),
            )
        )

    def __radd__(self, value: str) -> HTMLFormatter:
        """Returns value+self."""
        return HTMLFormatter(FormatString.__add__(FormatString(value), self).as_str())

    def as_str(self) -> str:
        """Returns self as a standart string."""
        return self.__str__()

    def format(self, *args: object, **kwargs: object) -> "HTMLFormatter":
        return self.STRING_FORMATTER.format(self, *args, **kwargs)


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

    PARSE_MODE = ParseMode.HTML


def escape(string: str) -> EscapedString:
    if isinstance(string, EscapedString | HTMLFormatter):
        return EscapedString(string)
    return EscapedString(html.escape(string, quote=False))


def block_quote(string: str, expandable: bool = False) -> TagFormat:
    return TagFormat(
        string,
        tag="blockquote",
        **{} if not expandable else {"expandable": None},
    )


def bold(string: str) -> TagFormat:
    return TagFormat(string, tag="b")


def code_inline(string: str) -> TagFormat:
    return TagFormat(string, tag="code")


def italic(string: str) -> TagFormat:
    return TagFormat(string, tag="i")


def link(href: str, string: str | None = None) -> TagFormat:
    return TagFormat(
        string or href,
        tag="a",
        href=QUOT_MARK + href + QUOT_MARK,
    )


def pre_code(string: str, lang: str | ProgrammingLanguage | None = None) -> TagFormat:
    if lang is None:
        return TagFormat(string, tag="pre")
    lang = lang.value if isinstance(lang, ProgrammingLanguage) else lang
    return pre_code(TagFormat(string, tag="code", **{"class": f"language-{lang}"}))


def spoiler(string: str) -> TagFormat:
    return TagFormat(string, tag="tg-spoiler")


def strike(string: str) -> TagFormat:
    return TagFormat(string, tag="s")


def mention(string: str, user_id: int) -> TagFormat:
    return link(tg_mention_link(user_id=user_id), string)


def tg_emoji(string: str, emoji_id: int) -> TagFormat:
    return TagFormat(string, tag="tg-emoji", emoji_id=emoji_id)


def underline(string: str) -> TagFormat:
    return TagFormat(string, tag="u")


__all__ = (
    "FormatString",
    "HTMLFormatter",
    "SpecialFormat",
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
